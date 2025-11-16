import pandas as pd

# Load the most recent CSV
df = pd.read_csv("../data/raw/powerball_20_pages_2025-11-16_07-13-21.csv")

# Quick check
print(df.head())
