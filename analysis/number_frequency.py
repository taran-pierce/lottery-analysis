import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths
DATA_FILE = os.path.join("data", "raw", "latest.csv")
CHARTS_DIR = os.path.join("charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# Load CSV
df = pd.read_csv(DATA_FILE)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'], format="%A, %m/%d/%y")

# Make sure month_year is a string (seaborn likes that)
df['month_year'] = df['date'].dt.to_period('M').astype(str)

# --------------------------
# White Ball Frequency Bar Chart
# --------------------------
white_numbers = df[['white_1', 'white_2', 'white_3', 'white_4', 'white_5']].values.flatten()
white_counts = pd.Series(white_numbers).value_counts().sort_index()

plt.figure(figsize=(12, 6))
white_counts.plot(kind='bar')
plt.title("Frequency of White Ball Numbers")
plt.xlabel("Number")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "white_ball_frequency.png"))
plt.close()

# --------------------------
# Powerball Frequency Bar Chart
# --------------------------
power_counts = df['powerball'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
power_counts.plot(kind='bar', color='red')
plt.title("Frequency of Powerball Numbers")
plt.xlabel("Number")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "powerball_frequency.png"))
plt.close()

# --------------------------
# White Ball Position Heatmap
# --------------------------
positions = ['white_1', 'white_2', 'white_3', 'white_4', 'white_5']
heatmap_data = pd.DataFrame(index=range(1, 70), columns=positions).fillna(0)

for pos in positions:
    counts = df[pos].value_counts()
    for number, count in counts.items():
        heatmap_data.at[number, pos] = count

plt.figure(figsize=(12, 10))
sns.heatmap(heatmap_data.astype(int), cmap="YlGnBu", linewidths=.5, annot=True, fmt="d")
plt.title("Heatmap of White Ball Numbers by Position")
plt.xlabel("Position")
plt.ylabel("White Ball Number")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "white_ball_heatmap.png"))
plt.close()

# --------------------------
# Trends Over Time - White Balls
# --------------------------
# Prepare trend data
trend_list = []

for pos in positions:
    tmp = df.groupby('month_year')[pos].apply(lambda x: x.value_counts()).rename_axis(['month_year', 'number']).reset_index(name='count')
    tmp['position'] = pos
    trend_list.append(tmp)

trend_data = pd.concat(trend_list, ignore_index=True)

# Pivot table: rows=month_year, columns=number, values=sum of counts
trend_pivot = trend_data.pivot_table(index='month_year', columns='number', values='count', aggfunc='sum', fill_value=0)

# Now all columns are numeric
trend_pivot = trend_pivot.astype(int)

# Plot
plt.figure(figsize=(14, 8))
sns.lineplot(data=trend_pivot)
plt.title("Trends Over Time - White Ball Numbers (Monthly)")
plt.xlabel("Month-Year")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.legend(title='Number', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "white_ball_trends.png"))
plt.close()

# --------------------------
# Trends Over Time - Powerball
# --------------------------
power_trend = df.groupby('month_year')['powerball'].apply(lambda x: x.value_counts()).unstack(fill_value=0)

power_trend = power_trend.fillna(0).astype(int)

plt.figure(figsize=(14, 8))
sns.lineplot(data=power_trend, palette="Reds_r")
plt.title("Trends Over Time - Powerball Numbers (Monthly)")
plt.xlabel("Month-Year")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.legend(title='Number', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "powerball_trends.png"))
plt.close()

print(f"All charts, including trends over time, saved to {CHARTS_DIR}")
