import pandas as pd

# Load the most recent CSV
df = pd.read_csv("../data/raw/latest.csv")

# Quick check
print(df.head())
