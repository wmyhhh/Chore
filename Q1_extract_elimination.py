import pandas as pd
import re

def parse_elimination(val):
    if pd.isna(val):
        return None
    val = str(val).strip()
    
    # Pattern for "Eliminated Week X"
    match = re.search(r'Eliminated Week (\d+)', val, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Handle placements
    if "1st Place" in val or "Winner" in val:
        return "Champion"
    if "2nd Place" in val or "Runner-up" in val:
        return "Runner-up"
    if "3rd Place" in val:
        return "3rd Place"
        
    return val

def main():
    input_path = r'd:\Study\Maths\MCM\2026C\2026_MCM_Problem_C_Data.csv'
    output_path = r'd:\Study\Maths\MCM\2026C\Q1_elimination_week.csv'
    
    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Create new dataframe
    result_df = pd.DataFrame()
    result_df['season'] = df['season']
    result_df['celebrity'] = df['celebrity_name']
    result_df['eliminated_week'] = df['results'].apply(parse_elimination)
    
    # Save
    result_df.to_csv(output_path, index=False)
    print(f"Processed {len(result_df)} rows. Saved to {output_path}")
    print("Sample output:")
    print(result_df.head(10))

if __name__ == '__main__':
    main()
