# Step 1: import the libraries
import pandas as pd
import matplotlib.pyplot as plt

# Step 2: read your CSV
df = pd.read_csv("../data/raw/latest.csv")

# Step 3: combine all white balls into a single list
white_numbers = df[['white_1', 'white_2', 'white_3', 'white_4', 'white_5']].values.flatten()

# Step 4: count occurrences
white_counts = pd.Series(white_numbers).value_counts().sort_index()

# Step 5: plot the frequency of white ball numbers
plt.figure(figsize=(12, 6))
white_counts.plot(kind='bar')
plt.title("Frequency of White Ball Numbers")
plt.xlabel("Number")
plt.ylabel("Count")
plt.show()

power_counts = df['powerball'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
power_counts.plot(kind='bar', color='red')
plt.title("Frequency of Powerball Numbers")
plt.xlabel("Number")
plt.ylabel("Count")
plt.show()
