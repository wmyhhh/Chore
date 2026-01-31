import pandas as pd

# 读取原始数据
df = pd.read_csv('2026_MCM_Problem_C_Data.csv')

# 准备存储结果的列表
elimination_data = []

# 遍历每一行（每个参赛选手）
for idx, row in df.iterrows():
    celebrity = row['celebrity_name']
    season = row['season']
    results = row['results']
    
    # 确定淘汰周数
    eliminated_week = None
    
    # 从results字段提取淘汰信息
    if 'Eliminated Week' in results:
        # 提取周数，例如 "Eliminated Week 3" -> 3
        try:
            week_str = results.split('Week')[1].strip()
            eliminated_week = int(week_str.split()[0])
        except:
            eliminated_week = None
    elif 'Withdrew' in results:
        # 找到最后一个有评分的周
        for week in range(1, 12):
            has_score = False
            for judge in range(1, 5):
                col_name = f'week{week}_judge{judge}_score'
                if col_name in df.columns:
                    score = row[col_name]
                    if pd.notna(score) and score != 'N/A' and score != 0:
                        has_score = True
                        break
            if has_score:
                eliminated_week = week
        eliminated_week = f"Withdrew Week {eliminated_week}" if eliminated_week else "Withdrew"
    elif '1st Place' in results:
        eliminated_week = '冠军 (Champion)'
    elif '2nd Place' in results:
        eliminated_week = '亚军 (Runner-up)'
    elif '3rd Place' in results:
        eliminated_week = '季军 (3rd Place)'
    else:
        # 其他情况，尝试找到最后有评分的周
        last_week_with_score = None
        for week in range(1, 12):
            has_score = False
            for judge in range(1, 5):
                col_name = f'week{week}_judge{judge}_score'
                if col_name in df.columns:
                    score = row[col_name]
                    if pd.notna(score) and score != 'N/A' and score != 0:
                        has_score = True
                        break
            if has_score:
                last_week_with_score = week
        
        if last_week_with_score:
            # 检查是否是最后一周还有比赛的（可能是决赛选手）
            eliminated_week = last_week_with_score
    
    # 添加到结果
    elimination_data.append({
        'season': season,
        'celebrity': celebrity,
        'eliminated_week': eliminated_week,
        'results': results
    })

# 创建结果DataFrame
result_df = pd.DataFrame(elimination_data)

# 按season和eliminated_week排序
# 对于数字类型的周数进行排序，对于字符串类型的放在最后
result_df['sort_key'] = result_df['eliminated_week'].apply(
    lambda x: (0, x) if isinstance(x, int) else (1, str(x))
)
result_df = result_df.sort_values(['season', 'sort_key']).reset_index(drop=True)
result_df = result_df.drop('sort_key', axis=1)

# 保存为CSV文件
result_df.to_csv('elimination_summary.csv', index=False)

print("淘汰信息整理完成！")
print(f"总共 {len(result_df)} 位选手")
print(f"\n各赛季参赛人数统计：")
print(result_df.groupby('season').size())

print(f"\n前20行数据预览：")
print(result_df.head(20).to_string())

# 按赛季分别显示
print("\n" + "="*80)
print("各赛季淘汰详情：")
print("="*80)
for season in sorted(result_df['season'].unique()):
    season_data = result_df[result_df['season'] == season]
    print(f"\n第 {season} 赛季：")
    print("-" * 80)
    for idx, row in season_data.iterrows():
        print(f"  {row['celebrity']:<30} 淘汰周数: {row['eliminated_week']:<20} ({row['results']})")
