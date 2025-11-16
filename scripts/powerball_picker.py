#!/usr/bin/env python3

import pandas as pd
import argparse
import numpy as np
import os
import random

# Paths
DATA_FILE = os.path.join("data", "raw", "latest.csv")

# --------------------------
# CLI Arguments
# --------------------------
parser = argparse.ArgumentParser(description="Generate fun Powerball number picks based on historical data")
parser.add_argument("--picks", type=int, default=1, help="Number of picks to generate")
parser.add_argument("--strategy", type=str, choices=["hot", "cold", "mixed"], default="mixed",
                    help="Strategy for picking numbers: hot, cold, or mixed")
args = parser.parse_args()

# --------------------------
# Load CSV
# --------------------------
df = pd.read_csv(DATA_FILE)
white_positions = ['white_1', 'white_2', 'white_3', 'white_4', 'white_5']

# Build set of existing combinations to avoid repeats
existing_combos = set(tuple(sorted(row[white_positions].values)) + (row['powerball'],) for _, row in df.iterrows())

# --------------------------
# ANSI colors
# --------------------------
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# --------------------------
# Helper functions
# --------------------------
def get_position_frequencies(df, positions):
    freq_dict = {}
    for pos in positions:
        freq_dict[pos] = df[pos].value_counts().sort_index()
    return freq_dict

white_position_freqs = get_position_frequencies(df, white_positions)
power_counts = df['powerball'].value_counts().sort_index()

def pick_number_with_weights(counts, strategy="mixed"):
    numbers = counts.index.tolist()
    freqs = counts.values.astype(float)
    if strategy == "hot":
        weights = freqs
    elif strategy == "cold":
        weights = 1 / (freqs + 1)
    else:  # mixed
        weights = freqs + 1 / (freqs + 1)
    weights = weights / weights.sum()
    return np.random.choice(numbers, p=weights)

# --------------------------
# Generate picks
# --------------------------
all_picks = []
attempts = 0
max_attempts = 1000

while len(all_picks) < args.picks and attempts < max_attempts:
    attempts += 1
    pick_desc = []
    white_balls = []

    for pos in white_positions:
        num = pick_number_with_weights(white_position_freqs[pos], strategy=args.strategy)
        white_balls.append(num)
        freq = white_position_freqs[pos].get(num, 0)
        if freq >= white_position_freqs[pos].mean():
            pick_desc.append(f"{GREEN}{num} (hot in {pos}){RESET}")
        else:
            pick_desc.append(f"{RED}{num} (cold in {pos}){RESET}")

    white_balls_sorted = sorted(white_balls)
    powerball = pick_number_with_weights(power_counts, strategy=args.strategy)
    pb_freq = power_counts.get(powerball, 0)
    pb_desc = f"{GREEN}{powerball} (hot){RESET}" if pb_freq >= power_counts.mean() else f"{RED}{powerball} (cold){RESET}"

    combo_tuple = tuple(white_balls_sorted) + (powerball,)
    if combo_tuple not in existing_combos:
        all_picks.append((white_balls_sorted, powerball, pick_desc, pb_desc))
        existing_combos.add(combo_tuple)

# --------------------------
# Print picks with colorful, bulleted reasons
# --------------------------
print(f"\n{BOLD}Generated {len(all_picks)} Powerball pick(s) using '{args.strategy}' strategy:{RESET}\n")
for idx, (whites, pb, desc, pb_desc) in enumerate(all_picks, 1):
    print(f"{BOLD}Pick {idx}:{RESET} Whites: {', '.join(map(str, whites))} | Powerball: {pb}")
    print("  Reasons:")
    for d in desc:
        print(f"    • {d}")
    print(f"    • Powerball: {pb_desc}\n")

print(f"{BOLD}Have fun and good luck! 🍀{RESET}")
