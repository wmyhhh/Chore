"""
Fan Vote Estimation Consistency Metrics
=======================================

This script implements multiple measures to evaluate whether estimated fan votes
lead to results consistent with actual eliminations.

Metrics Implemented:
1. Rule Consistency (Constraint Satisfaction)
   - Violation Count: How many weeks the model fails to predict the correct elimination
   - Satisfaction Rate: Percentage of weeks where constraints are satisfied

2. Margin of Elimination (Δ_w)
   - Measures how "confident" the model is about each elimination
   - Δ > 0 means eliminated person has lowest score (correct)
   - Larger Δ means more stable/confident prediction

3. Ranking Consistency
   - Pairwise Violation Rate: Among all (eliminated, other) pairs, how often does
     the model incorrectly rank the eliminated person higher?
   - Kendall's tau (partial): Correlation between model ranking and elimination order

Author: MCM 2026 Analysis
"""

import pandas as pd
import numpy as np
import os
from scipy import stats

def load_data():
    base_dir = r'd:\Study\Maths\MCM\2026C'
    path_data = os.path.join(base_dir, 'Q1_data.csv')
    path_fan = os.path.join(base_dir, 'fan_votes_percentage.csv')
    path_elim = os.path.join(base_dir, 'Q1_elimination_week.csv')
    
    try:
        df_data = pd.read_csv(path_data)
        df_fan = pd.read_csv(path_fan)
        df_elim = pd.read_csv(path_elim)
        return df_data, df_fan, df_elim, base_dir
    except Exception as e:
        print(f"Error loading files: {e}")
        return None, None, None, None

def get_elimination_map(df_elim):
    """
    Returns: dict (season, week) -> [list of eliminated celebrities]
    """
    elim_map = {}
    
    def clean_week(x):
        try:
            return int(float(x))
        except:
            return None

    df_elim['clean_week'] = df_elim['eliminated_week'].apply(clean_week)
    
    for _, row in df_elim.iterrows():
        s = row['season']
        w = row['clean_week']
        c = row['celebrity']
        
        if pd.notna(w) and pd.notna(s):
            key = (int(s), int(w))
            if key not in elim_map:
                elim_map[key] = []
            elim_map[key].append(c)
            
    return elim_map

def compute_combined_score(cohort, season):
    """
    Compute combined score based on season-specific rules.
    
    Season 1-2: Rank Sum (Higher = Worse)
    Season 3-27: Percent Sum (Lower = Worse)
    Season 28-34: Rank Sum with Bottom-2 Hybrid (Higher = Worse)
    
    Returns cohort with:
    - 'FinalScore': The raw combined score
    - 'EliminationScore': Unified score where LOWER = MORE LIKELY TO BE ELIMINATED
    - 'method': String indicating which method was used
    """
    cohort = cohort.copy()
    
    if season in [1, 2]:
        # Rank Sum Method: Higher sum = Worse = More likely eliminated
        cohort['R_Judge'] = cohort['judge_score_total'].rank(ascending=False, method='min')
        cohort['R_Fan'] = cohort['FanVote%'].rank(ascending=False, method='min')
        cohort['FinalScore'] = cohort['R_Judge'] + cohort['R_Fan']
        
        # EliminationScore: negate so lower = more likely eliminated
        cohort['EliminationScore'] = -cohort['FinalScore']
        cohort['method'] = 'Rank Sum (S1-2)'
        
    elif season >= 28:
        # Season 28-34: Rank Sum with Hybrid Bottom-2
        cohort['R_Judge'] = cohort['judge_score_total'].rank(ascending=False, method='min')
        cohort['R_Fan'] = cohort['FanVote%'].rank(ascending=False, method='min')
        cohort['FinalScore'] = cohort['R_Judge'] + cohort['R_Fan']
        
        # EliminationScore: negate so lower = more likely eliminated
        cohort['EliminationScore'] = -cohort['FinalScore']
        cohort['method'] = 'Hybrid Bottom-2 (S28+)'
        
    else:  # Season 3-27: Percent Sum Method
        total_judge = cohort['judge_score_total'].sum()
        total_fan = cohort['FanVote%'].sum()
        
        if total_judge == 0: total_judge = 1
        if total_fan == 0: total_fan = 1
        
        cohort['P_Judge'] = (cohort['judge_score_total'] / total_judge) * 100
        cohort['P_Fan'] = (cohort['FanVote%'] / total_fan) * 100
        cohort['FinalScore'] = cohort['P_Judge'] + cohort['P_Fan']
        
        # EliminationScore: Lower PercentSum = worse = more likely eliminated
        # So EliminationScore = FinalScore directly (no negation needed)
        cohort['EliminationScore'] = cohort['FinalScore']
        cohort['method'] = 'Percent Sum (S3-27)'
    
    return cohort

def compute_metrics():
    df_data, df_fan, df_elim, base_dir = load_data()
    if df_data is None:
        return
    
    elim_map = get_elimination_map(df_elim)
    merged = pd.merge(df_data, df_fan, on=['season', 'week', 'celebrity'], how='inner')
    
    # Storage for metrics
    week_results = []
    
    sorted_events = sorted(elim_map.keys())
    
    for (s, w) in sorted_events:
        actual_eliminated = elim_map[(s, w)]
        
        cohort = merged[(merged['season'] == s) & (merged['week'] == w)].copy()
        
        if cohort.empty:
            continue
        
        # Find valid eliminated people in this cohort
        valid_elim = [p for p in actual_eliminated if p in cohort['celebrity'].values]
        if not valid_elim:
            continue
        
        # Compute combined score
        cohort = compute_combined_score(cohort, s)
        
        n_candidates = len(cohort)
        n_eliminated = len(valid_elim)
        
        # --- METRIC 1: Constraint Satisfaction ---
        # For each eliminated person e, check if S_e <= S_i for all i != e
        # (Using EliminationScore where lower = more likely eliminated)
        
        violations = 0
        satisfied = True
        
        for e in valid_elim:
            e_score = cohort[cohort['celebrity'] == e]['EliminationScore'].values[0]
            other_scores = cohort[cohort['celebrity'] != e]['EliminationScore'].values
            
            # e should have the MINIMUM score (most likely to be eliminated)
            # Violation: if e_score > min(other_scores), someone else should have been eliminated first
            # Actually, constraint is: e_score <= all other scores
            # Violation count = number of people with score < e_score (they should have gone first)
            violations_for_e = np.sum(other_scores < e_score)
            violations += violations_for_e
            
            if violations_for_e > 0:
                satisfied = False
        
        # --- METRIC 2: Margin of Elimination (Δ_w) ---
        # Δ_w = min_{i != e} (S_i - S_e)
        # If Δ_w > 0, e has the lowest score (correct)
        # If Δ_w <= 0, someone else had lower or equal score (violation)
        
        margins = []
        for e in valid_elim:
            e_score = cohort[cohort['celebrity'] == e]['EliminationScore'].values[0]
            other_scores = cohort[cohort['celebrity'] != e]['EliminationScore'].values
            
            if len(other_scores) > 0:
                margin = np.min(other_scores) - e_score
                margins.append(margin)
        
        avg_margin = np.mean(margins) if margins else 0
        min_margin = np.min(margins) if margins else 0
        
        # --- METRIC 3: Pairwise Violation Rate ---
        # For each pair (e, i) where e is eliminated and i is not:
        # Violation if model says S_e > S_i (e should have lower score)
        
        total_pairs = 0
        violated_pairs = 0
        
        for e in valid_elim:
            e_score = cohort[cohort['celebrity'] == e]['EliminationScore'].values[0]
            
            for idx, row in cohort.iterrows():
                if row['celebrity'] != e and row['celebrity'] not in valid_elim:
                    total_pairs += 1
                    # Violation: e_score > other_score (e shouldn't be higher)
                    if e_score > row['EliminationScore']:
                        violated_pairs += 1
        
        pairwise_violation_rate = violated_pairs / total_pairs if total_pairs > 0 else 0
        
        # Store results
        method_str = cohort['method'].iloc[0] if 'method' in cohort.columns else 'Unknown'
        week_results.append({
            'season': s,
            'week': w,
            'method': method_str,
            'n_candidates': n_candidates,
            'n_eliminated': n_eliminated,
            'eliminated': ', '.join(valid_elim),
            'constraint_satisfied': 1 if satisfied else 0,
            'violation_count': violations,
            'margin_min': min_margin,
            'margin_avg': avg_margin,
            'pairwise_total': total_pairs,
            'pairwise_violated': violated_pairs,
            'pairwise_violation_rate': pairwise_violation_rate
        })
    
    df_results = pd.DataFrame(week_results)
    
    # --- SUMMARY STATISTICS ---
    print("\n" + "="*80)
    print("CONSISTENCY METRICS SUMMARY")
    print("="*80)
    
    # Overall
    total_weeks = len(df_results)
    satisfied_weeks = df_results['constraint_satisfied'].sum()
    
    print(f"\n[1] RULE CONSISTENCY (Constraint Satisfaction)")
    print(f"    Total Elimination Events: {total_weeks}")
    print(f"    Constraints Satisfied: {satisfied_weeks}/{total_weeks} = {satisfied_weeks/total_weeks:.2%}")
    print(f"    Total Violations: {df_results['violation_count'].sum()}")
    
    print(f"\n[2] MARGIN OF ELIMINATION (Δ_w)")
    print(f"    Mean Margin (across all weeks): {df_results['margin_avg'].mean():.4f}")
    print(f"    Min Margin (worst case): {df_results['margin_min'].min():.4f}")
    print(f"    Weeks with Positive Margin (Δ>0): {(df_results['margin_min'] > 0).sum()}/{total_weeks}")
    
    # Categorize margins
    close_calls = df_results[(df_results['margin_min'] > 0) & (df_results['margin_min'] < 0.05)]
    confident = df_results[df_results['margin_min'] >= 0.05]
    print(f"    - 'Close Calls' (0 < Δ < 0.05): {len(close_calls)} weeks")
    print(f"    - 'Confident' (Δ >= 0.05): {len(confident)} weeks")
    
    print(f"\n[3] PAIRWISE VIOLATION RATE")
    total_pairs = df_results['pairwise_total'].sum()
    violated_pairs = df_results['pairwise_violated'].sum()
    print(f"    Total Pairs Checked: {total_pairs}")
    print(f"    Violated Pairs: {violated_pairs}")
    print(f"    Overall Pairwise Violation Rate: {violated_pairs/total_pairs:.2%}" if total_pairs > 0 else "    N/A")
    
    # --- BY SEASON GROUP ---
    print("\n" + "-"*80)
    print("BREAKDOWN BY SEASON GROUP")
    print("-"*80)
    
    groups = [
        ("Seasons 1-2 (Rank)", df_results[df_results['season'].isin([1, 2])]),
        ("Seasons 3-27 (Percent)", df_results[(df_results['season'] >= 3) & (df_results['season'] <= 27)]),
        ("Seasons 28-34 (Hybrid)", df_results[df_results['season'] >= 28])
    ]
    
    for name, g in groups:
        if len(g) == 0:
            continue
        sat_rate = g['constraint_satisfied'].mean()
        avg_margin = g['margin_avg'].mean()
        pv_rate = g['pairwise_violated'].sum() / g['pairwise_total'].sum() if g['pairwise_total'].sum() > 0 else 0
        
        print(f"\n  [{name}]")
        print(f"    Events: {len(g)}")
        print(f"    Constraint Satisfaction Rate: {sat_rate:.2%}")
        print(f"    Average Margin: {avg_margin:.4f}")
        print(f"    Pairwise Violation Rate: {pv_rate:.2%}")
    
    # Save detailed results
    output_path = os.path.join(base_dir, 'consistency_metrics_detailed.csv')
    df_results.to_csv(output_path, index=False)
    print(f"\n\nDetailed results saved to: {output_path}")
    
    return df_results

if __name__ == '__main__':
    compute_metrics()
