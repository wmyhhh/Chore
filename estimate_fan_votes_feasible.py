"""
Fan Vote Estimation using Feasible Region + Maximum Entropy Optimization
=========================================================================

This script estimates fan vote shares for each week using:
1. Feasible Region: Constraints derived from elimination results
2. Representative Solution: Maximum entropy optimization (least biased estimate)

Season-Specific Rules:
- Seasons 1-2: Rank Sum (Higher rank sum = Worse)
- Seasons 3-27: Percent Sum (Lower percent sum = Worse)  
- Seasons 28-34: Rank Sum with Hybrid Bottom-2

Author: MCM 2026 Analysis
"""

import pandas as pd
import numpy as np
from scipy.optimize import minimize, LinearConstraint, NonlinearConstraint
from itertools import permutations
import os
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# DATA LOADING
# =============================================================================

def load_data():
    base_dir = r'd:\Study\Maths\MCM\2026C'
    path_data = os.path.join(base_dir, 'Q1_data.csv')
    path_elim = os.path.join(base_dir, 'Q1_elimination_week.csv')
    
    try:
        df_data = pd.read_csv(path_data)
        df_elim = pd.read_csv(path_elim)
        return df_data, df_elim, base_dir
    except Exception as e:
        print(f"Error loading files: {e}")
        return None, None, None

def get_elimination_map(df_elim):
    """Returns dict: (season, week) -> [eliminated celebrities]"""
    elim_map = {}
    
    def clean_week(x):
        try:
            return int(float(x))
        except:
            return None

    df_elim['clean_week'] = df_elim['eliminated_week'].apply(clean_week)
    
    for _, row in df_elim.iterrows():
        s, w, c = row['season'], row['clean_week'], row['celebrity']
        if pd.notna(w) and pd.notna(s):
            key = (int(s), int(w))
            if key not in elim_map:
                elim_map[key] = []
            elim_map[key].append(c)
    return elim_map

# =============================================================================
# OPTIMIZATION: PERCENT-BASED (Seasons 3-27)
# =============================================================================

def estimate_percent_based(cohort, elim_indices, judge_scores):
    """
    Percent-based method (S3-27):
    Combined Score = Judge% + Fan%
    Eliminated person has LOWEST combined score.
    
    Constraints: C_e <= C_i for all i != e
    => (J_e/sum_J + V_e) <= (J_i/sum_J + V_i)
    => V_e - V_i <= (J_i - J_e) / sum_J
    """
    n = len(cohort)
    sum_J = np.sum(judge_scores)
    if sum_J == 0: sum_J = 1
    
    judge_pct = judge_scores / sum_J
    
    # Objective: Maximum Entropy = -sum(V * log(V))
    # We minimize the negative entropy
    def neg_entropy(V):
        V_safe = np.clip(V, 1e-10, 1)
        return np.sum(V_safe * np.log(V_safe))
    
    def neg_entropy_grad(V):
        V_safe = np.clip(V, 1e-10, 1)
        return np.log(V_safe) + 1
    
    # Constraint: sum(V) = 1
    eq_constraint = {'type': 'eq', 'fun': lambda V: np.sum(V) - 1}
    
    # Inequality constraints: V_e - V_i <= (J_i - J_e) / sum_J for all i != e
    ineq_constraints = []
    for e_idx in elim_indices:
        for i in range(n):
            if i != e_idx and i not in elim_indices:
                diff = (judge_pct[i] - judge_pct[e_idx])
                # V_e - V_i <= diff  =>  V_e - V_i - diff <= 0
                ineq_constraints.append({
                    'type': 'ineq',
                    'fun': lambda V, e=e_idx, other=i, d=diff: d - (V[e] - V[other])
                })
    
    # Bounds: V_i >= 0
    bounds = [(1e-6, 1) for _ in range(n)]
    
    # Initial guess: uniform
    V0 = np.ones(n) / n
    
    result = minimize(
        neg_entropy, V0,
        method='SLSQP',
        bounds=bounds,
        constraints=[eq_constraint] + ineq_constraints,
        options={'maxiter': 500, 'ftol': 1e-9}
    )
    
    if result.success:
        return result.x
    else:
        # Fallback: return uniform
        return np.ones(n) / n

# =============================================================================
# OPTIMIZATION: RANK-BASED (Seasons 1-2, 28-34)
# =============================================================================

def estimate_rank_based(cohort, elim_indices, judge_scores):
    """
    Rank-based method (S1-2, S28+):
    Combined Rank = Judge_Rank + Fan_Rank
    Eliminated person has HIGHEST combined rank (worst).
    
    This is a discrete optimization problem. We:
    1. Enumerate feasible fan rank permutations
    2. For each feasible permutation, solve max entropy for vote shares
    3. Aggregate results (mean across feasible solutions)
    """
    n = len(cohort)
    
    # Compute judge ranks (1 = best, n = worst)
    # Higher score = lower rank number
    judge_ranks = n + 1 - np.argsort(np.argsort(-judge_scores)) 
    # Simpler: use pandas-style ranking
    temp_df = pd.DataFrame({'score': judge_scores})
    judge_ranks = temp_df['score'].rank(ascending=False, method='min').values
    
    # Find feasible fan rank permutations
    feasible_perms = []
    
    for perm in permutations(range(1, n + 1)):
        fan_ranks = np.array(perm)
        combined = judge_ranks + fan_ranks
        max_combined = np.max(combined)
        
        # Check: all eliminated people must have max combined rank
        is_feasible = True
        for e_idx in elim_indices:
            if combined[e_idx] < max_combined:
                is_feasible = False
                break
        
        if is_feasible:
            feasible_perms.append(perm)
    
    if not feasible_perms:
        # No feasible solution found - return uniform
        return np.ones(n) / n
    
    # Sample if too many (for efficiency)
    MAX_PERMS = 100
    if len(feasible_perms) > MAX_PERMS:
        import random
        feasible_perms = random.sample(feasible_perms, MAX_PERMS)
    
    # For each feasible permutation, solve max entropy with ordering constraints
    all_solutions = []
    
    for perm in feasible_perms:
        V = solve_max_entropy_with_ordering(n, perm)
        if V is not None:
            all_solutions.append(V)
    
    if not all_solutions:
        return np.ones(n) / n
    
    # Return mean across all feasible solutions
    return np.mean(all_solutions, axis=0)

def solve_max_entropy_with_ordering(n, rank_perm):
    """
    Given a fan rank permutation, find vote shares V such that:
    - sum(V) = 1, V >= 0
    - V respects the ordering: rank_perm[i] < rank_perm[j] => V[i] > V[j]
    - Maximize entropy
    """
    EPSILON = 1e-4
    
    # rank_perm[i] is the rank of contestant i (1 = best fan rank)
    # Lower rank => higher votes
    # So if rank_perm[i] < rank_perm[j], then V[i] > V[j]
    
    def neg_entropy(V):
        V_safe = np.clip(V, 1e-10, 1)
        return np.sum(V_safe * np.log(V_safe))
    
    constraints = [{'type': 'eq', 'fun': lambda V: np.sum(V) - 1}]
    
    # Ordering constraints
    for i in range(n):
        for j in range(n):
            if i != j and rank_perm[i] < rank_perm[j]:
                # V[i] > V[j] + epsilon
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda V, a=i, b=j: V[a] - V[b] - EPSILON
                })
    
    bounds = [(1e-6, 1) for _ in range(n)]
    V0 = np.ones(n) / n
    
    result = minimize(
        neg_entropy, V0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        options={'maxiter': 300}
    )
    
    return result.x if result.success else None

# =============================================================================
# MAIN ESTIMATION PIPELINE
# =============================================================================

def estimate_all_fan_votes():
    df_data, df_elim, base_dir = load_data()
    if df_data is None:
        return
    
    elim_map = get_elimination_map(df_elim)
    
    all_results = []
    
    # Get all unique (season, week) from data
    grouped = df_data.groupby(['season', 'week'])
    
    for (season, week), cohort in grouped:
        cohort = cohort.copy().reset_index(drop=True)
        n = len(cohort)
        
        if n < 2:
            continue
        
        celebrities = cohort['celebrity'].tolist()
        judge_scores = cohort['judge_score_total'].fillna(0).values
        
        # Check if this week has elimination
        key = (int(season), int(week))
        if key in elim_map:
            eliminated = elim_map[key]
            # Find indices of eliminated people
            elim_indices = [i for i, c in enumerate(celebrities) if c in eliminated]
            
            if not elim_indices:
                # Eliminated person not in cohort - skip or use uniform
                V_est = np.ones(n) / n
            else:
                # Estimate based on season-specific method
                if season in [1, 2] or season >= 28:
                    V_est = estimate_rank_based(cohort, elim_indices, judge_scores)
                else:
                    V_est = estimate_percent_based(cohort, elim_indices, judge_scores)
        else:
            # No elimination this week - use uniform (no information)
            V_est = np.ones(n) / n
        
        # Store results
        for i in range(n):
            all_results.append({
                'season': int(season),
                'week': int(week),
                'celebrity': celebrities[i],
                'judge_score': judge_scores[i],
                'FanVote%': V_est[i] * 100,  # Convert to percentage
                'method': 'Rank' if (season in [1, 2] or season >= 28) else 'Percent'
            })
        
        # Progress indicator
        if week == 1:
            print(f"Processing Season {season}...")
    
    # Save results
    df_results = pd.DataFrame(all_results)
    output_path = os.path.join(base_dir, 'fan_votes_feasible_region.csv')
    df_results.to_csv(output_path, index=False)
    
    print(f"\n{'='*60}")
    print(f"Fan Vote Estimation Complete")
    print(f"{'='*60}")
    print(f"Total records: {len(df_results)}")
    print(f"Seasons covered: {df_results['season'].nunique()}")
    print(f"Output saved to: {output_path}")
    
    # Summary statistics
    print(f"\n{'='*60}")
    print("Summary by Method:")
    print(f"{'='*60}")
    for method in ['Rank', 'Percent']:
        subset = df_results[df_results['method'] == method]
        if len(subset) > 0:
            print(f"\n[{method} Method]")
            print(f"  Records: {len(subset)}")
            print(f"  Mean FanVote%: {subset['FanVote%'].mean():.2f}%")
            print(f"  Std FanVote%: {subset['FanVote%'].std():.2f}%")
    
    return df_results

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    estimate_all_fan_votes()
