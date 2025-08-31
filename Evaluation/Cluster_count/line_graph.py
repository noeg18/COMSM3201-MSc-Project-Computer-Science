import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
   print("Error: missing input file")
   sys.exit(1)

df = pd.read_csv(sys.argv[1])
df['correctness'] = pd.to_numeric(df['correctness'].str.replace('%',''), errors='coerce')

# compute average cluster by correctness
avg_cluster = df.groupby('correctness', as_index=False)['cluster'].mean().sort_values('correctness')

# plot line graph
sns.set_style("whitegrid")
plt.figure(figsize=(8,6))
sns.lineplot(x='correctness', y='cluster', data=avg_cluster, marker='o')
plt.xlabel("Correctness (%)", fontsize=12)
plt.ylabel("Average Cluster Count", fontsize=12)
plt.title("Average Cluster Count by Correctness", fontsize=14)
plt.tight_layout()
plt.show()

