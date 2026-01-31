import pandas as pd

# 读取CSV文件
df = pd.read_csv('elimination_summary.csv')

# 只保留前3列
df = df[['season', 'celebrity', 'eliminated_week']]

# 保存回CSV文件
df.to_csv('elimination_summary.csv', index=False)

print("已删除results列！")
print(f"现在只有 {len(df.columns)} 列：{list(df.columns)}")
print(f"\n前10行数据预览：")
print(df.head(10))
