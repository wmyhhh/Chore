import pandas as pd
import numpy as np

# 读取原始数据
df = pd.read_csv('2026_MCM_Problem_C_Data.csv')

# 准备存储结果的列表
result_data = []

# 获取所有可能的周数（从列名中提取）
weeks = []
for col in df.columns:
    if col.startswith('week') and 'judge1' in col:
        week_num = int(col.split('_')[0].replace('week', ''))
        if week_num not in weeks:
            weeks.append(week_num)
weeks.sort()

# 遍历每一行（每个参赛选手）
for idx, row in df.iterrows():
    celebrity = row['celebrity_name']
    season = row['season']
    results = row['results']
    
    # 对每一周进行处理
    for week in weeks:
        # 获取该周所有评委的评分
        judge_scores = []
        for judge in range(1, 5):  # 假设最多4个评委
            col_name = f'week{week}_judge{judge}_score'
            if col_name in df.columns:
                score = row[col_name]
                # 只添加有效分数（不是0, N/A, 或空值）
                if pd.notna(score) and score != 'N/A' and score != 0:
                    try:
                        judge_scores.append(float(score))
                    except:
                        pass
        
        # 如果该周有评分，计算总分
        if judge_scores:
            judge_score_total = sum(judge_scores)
            
            # 判断该周是否被淘汰
            # 检查下一周是否全为0或N/A（表示被淘汰）
            eliminated_flag = 0
            
            # 如果结果中包含特定的周数淘汰信息
            if f'Week {week}' in results:
                eliminated_flag = 1
            elif week < max(weeks):
                # 检查下一周是否有分数
                next_week_has_score = False
                for judge in range(1, 5):
                    next_col = f'week{week+1}_judge{judge}_score'
                    if next_col in df.columns:
                        next_score = row[next_col]
                        if pd.notna(next_score) and next_score != 'N/A' and next_score != 0:
                            next_week_has_score = True
                            break
                
                # 如果下一周没有分数，说明本周被淘汰
                if not next_week_has_score and judge_score_total > 0:
                    eliminated_flag = 1
            
            # 添加到结果
            result_data.append({
                'season': season,
                'week': week,
                'celebrity': celebrity,
                'judge_score_total': judge_score_total,
                'eliminated_flag': eliminated_flag
            })

# 创建结果DataFrame
result_df = pd.DataFrame(result_data)

# 按season, week, celebrity排序
result_df = result_df.sort_values(['season', 'week', 'celebrity']).reset_index(drop=True)

# 保存为CSV文件
result_df.to_csv('processed_data.csv', index=False)

print(f"数据整理完成！")
print(f"总共处理了 {len(result_df)} 条记录")
print(f"\n前10行数据预览：")
print(result_df.head(10))
print(f"\n数据统计：")
print(f"赛季数量: {result_df['season'].nunique()}")
print(f"参赛选手数量: {result_df['celebrity'].nunique()}")
print(f"周数范围: {result_df['week'].min()} - {result_df['week'].max()}")
print(f"\n被淘汰记录数: {result_df['eliminated_flag'].sum()}")
