import pandas as pd
import numpy as np
import os

def load_data():
    base_dir = r'd:\Study\Maths\MCM\2026C'
    path_data = os.path.join(base_dir, 'Q1_data.csv')
    path_fan = os.path.join(base_dir, 'fan_votes_percentage.csv')
    path_elim = os.path.join(base_dir, 'Q1_elimination_week.csv')
    
    try:
        df_data = pd.read_csv(path_data)
        df_fan = pd.read_csv(path_fan)
        df_elim = pd.read_csv(path_elim)
        return df_data, df_fan, df_elim
    except Exception as e:
        print(f"Error loading files: {e}")
        return None, None, None

def get_elimination_map(df_elim):
    """
    Returns a dictionary: (season, week) -> list of eliminated celebrities
    """
    elim_map = {}
    
    # Clean 'eliminated_week' - handle non-numeric values if any remain
    def clean_week(x):
        try:
            return float(x)
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

def validate_advanced():
    base_dir = r'd:\Study\Maths\MCM\2026C'
    df_data, df_fan, df_elim = load_data()
    if df_data is None: return

    elim_map = get_elimination_map(df_elim)
    
    # Merge Judge and Fan Data
    # Inner merge - we only validate where we have both
    merged = pd.merge(df_data, df_fan, on=['season', 'week', 'celebrity'], how='inner')
    
    results = []
    
    # Process each week found in the elimination map
    # Sort keys for consistent order
    sorted_events = sorted(elim_map.keys())
    
    for (s, w) in sorted_events:
        actual_eliminated = elim_map[(s, w)]
        num_eliminated = len(actual_eliminated)
        
        # Get cohort for this week
        cohort = merged[(merged['season'] == s) & (merged['week'] == w)].copy()
        
        # Validation checks
        if cohort.empty:
            continue
            
        # Ensure actual eliminated people are in the cohort
        valid_targets = [p for p in actual_eliminated if p in cohort['celebrity'].values]
        if not valid_targets:
            continue
            
        # Determine Method based on Season
        method = ""
        
        # --- CALCULATION ---
        
        # Metrics storage
        # We will add columns: 'metric_val', 'metric_rank'
        # High metric_rank (e.g. 1) = Best Performance? 
        # Wait, let's stick to "Score that determines elimination".
        # Let's define 'EliminationScore': The value where EXTREME (either High or Low) means elimination.
        
        # 1. Seasons 1-2: Combined Rank (Sum). Higher Sum = Worse.
        if s in [1, 2]:
            method = "Rank Sum (S1-2)"
            
            # Judge Rank (1 is Best, N is Worst)
            # method='min' -> Ties share the top rank (1, 2, 2, 4). 
            # This is standard.
            cohort['R_Judge'] = cohort['judge_score_total'].rank(ascending=False, method='min')
            
            # Fan Rank (1 is Best)
            cohort['R_Fan'] = cohort['FanVote%'].rank(ascending=False, method='min')
            
            # Combined
            cohort['Final_Score'] = cohort['R_Judge'] + cohort['R_Fan']
            
            # Worst = Highest Score
            # Sort Descending
            cohort = cohort.sort_values('Final_Score', ascending=False)
            
            # Predicted set: Top k candidates (including ties)
            # Find the k-th worst score
            unique_scores = sorted(cohort['Final_Score'].unique(), reverse=True)
            
            # We need to pick at least k people.
            # If k=1, we take people with Max Score.
            # If k=2, we take people with Max Score. If only 1 has Max, we take Next Max too.
            
            cutoff_val = -1
            count_so_far = 0
            for val in unique_scores:
                count = len(cohort[cohort['Final_Score'] == val])
                count_so_far += count
                cutoff_val = val
                if count_so_far >= num_eliminated:
                    break
            
            predicted_candidates = cohort[cohort['Final_Score'] >= cutoff_val]['celebrity'].tolist()
            
            
        # 2. Seasons 28-34: Hybrid / Rank (Bottom 2).
        elif s >= 28:
            method = "Hybrid Bottom 2 (S28+)"
            
            cohort['R_Judge'] = cohort['judge_score_total'].rank(ascending=False, method='min')
            cohort['R_Fan'] = cohort['FanVote%'].rank(ascending=False, method='min')
            cohort['Final_Score'] = cohort['R_Judge'] + cohort['R_Fan']
            
            # Worst = Highest Score
            cohort = cohort.sort_values('Final_Score', ascending=False)
            
            # Logic: Bottom 2 are identified.
            # We look for the worst 2 scores.
            unique_scores = sorted(cohort['Final_Score'].unique(), reverse=True)
            
            # We need the bottom 2 CANDIDATES, or the set of candidates falling in the Bottom 2 SLOTS.
            # If strict bottom 2:
            cutoff_val = -1
            count_so_far = 0
            target_count = 2 # Always identify bottom 2
            
            for val in unique_scores:
                count = len(cohort[cohort['Final_Score'] == val])
                count_so_far += count
                cutoff_val = val
                if count_so_far >= target_count:
                    break
            
            predicted_candidates = cohort[cohort['Final_Score'] >= cutoff_val]['celebrity'].tolist()
            
            
        # 3. Seasons 3-27: Percent. Lower Sum = Worse.
        else:
            method = "Percent Sum (S3-27)"
            
            # Calculate Percents
            total_judge_pts = cohort['judge_score_total'].sum()
            total_fan_pts = cohort['FanVote%'].sum() # Assuming this is raw sum
            
            # Avoid div by zero
            if total_judge_pts == 0: total_judge_pts = 1
            if total_fan_pts == 0: total_fan_pts = 1
            
            cohort['P_Judge'] = (cohort['judge_score_total'] / total_judge_pts) * 100
            cohort['P_Fan'] = (cohort['FanVote%'] / total_fan_pts) * 100
            
            cohort['Final_Score'] = cohort['P_Judge'] + cohort['P_Fan']
            
            # Worst = Lowest Score
            # Sort Ascending
            cohort = cohort.sort_values('Final_Score', ascending=True)
            
            unique_scores = sorted(cohort['Final_Score'].unique()) # Low to High
            
            cutoff_val = -1
            count_so_far = 0
            for val in unique_scores:
                count = len(cohort[cohort['Final_Score'] == val])
                count_so_far += count
                cutoff_val = val
                if count_so_far >= num_eliminated:
                    break
                    
            predicted_candidates = cohort[cohort['Final_Score'] <= cutoff_val]['celebrity'].tolist()

        # --- VALIDATION ---
        
        # Check if ANY of the actual targets are in the predicted set
        # (For S28+, if the eliminated person was in Bottom 2, it's a correct prediction of risk)
        
        matches = [p for p in valid_targets if p in predicted_candidates]
        is_match = len(matches) > 0
        
        # Check Tie-Breaker situations (Bonus)
        tie_note = ""
        if len(predicted_candidates) > num_eliminated and is_match:
            # We predicted more people than were eliminated (Tie).
            # And the actual person was in there.
            tie_note = " (Tie)"
            
        results.append({
            'season': s,
            'week': w,
            'method': method,
            'num_elim_actual': num_eliminated,
            'actual': str(valid_targets),
            'predicted': str(predicted_candidates),
            'match': 1 if is_match else 0,
            'note': tie_note,
            'candidates_count': len(cohort)
        })

    # --- REPORTING ---
    df_res = pd.DataFrame(results)
    
    # Save detailed
    df_res.to_csv(os.path.join(base_dir, 'validation_advanced_logic.csv'), index=False)
    
    print("\n" + "="*80)
    print("ADVANCED VALIDATION SUMMARY")
    print("="*80)
    
    if df_res.empty:
        print("No validation results generated.")
        return

    # Group 1: S1-2
    g1 = df_res[df_res['season'].isin([1, 2])]
    acc1 = g1['match'].mean() if len(g1) > 0 else 0
    print(f"\n[Seasons 1-2] Combined Rank Method")
    print(f"  Accuracy: {acc1:.2%} ({g1['match'].sum()}/{len(g1)})")
    
    # Group 2: S3-27
    g2 = df_res[(df_res['season'] >= 3) & (df_res['season'] <= 27)]
    acc2 = g2['match'].mean() if len(g2) > 0 else 0
    print(f"\n[Seasons 3-27] Combined Percent Method")
    print(f"  Accuracy: {acc2:.2%} ({g2['match'].sum()}/{len(g2)})")
    
    # Group 3: S28-34
    g3 = df_res[df_res['season'] >= 28]
    acc3 = g3['match'].mean() if len(g3) > 0 else 0
    print(f"\n[Seasons 28-34] Hybrid Bottom-2 Method")
    print(f"  Accuracy: {acc3:.2%} ({g3['match'].sum()}/{len(g3)})")
    
    print("\n" + "-"*80)
    print(f"Overall Accuracy: {df_res['match'].mean():.2%} ({df_res['match'].sum()}/{len(df_res)})")
    print(f"Detailed log saved to: validation_advanced_logic.csv")

if __name__ == '__main__':
    validate_advanced()
