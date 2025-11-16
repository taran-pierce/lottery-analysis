# Lottery Analysis

This repository contains scripts and analysis tools for gathering, visualizing, and generating Powerball number picks based on historical Colorado lottery data.

## Directory Structure

```
lottery-analysis/
├── analysis/
│   └── number_frequency.py       # Analyze number frequency, trends, and generate charts
├── data/
│   └── raw/
│       └── latest.csv            # Latest historical lottery data
├── scripts/
│   ├── powerball.py              # Scrape historical Powerball numbers from Colorado Lottery website
│   └── powerball_picker.py       # Generate fun Powerball number picks based on historical data
├── charts/                        # Generated charts from analysis
├── README.md
└── requirements.txt
```

````

## Setup

Install required packages:

```bash
pip install -r requirements.txt
````

## Scraping Historical Data

Use the `powerball.py` script to scrape historical Powerball numbers from the Colorado Lottery website.

```bash
python3 scripts/powerball.py --pages 5
```

* `--pages` specifies the number of pages to scrape.
* Output is saved to `data/raw/latest.csv`.
* The script also prints parsed draws to the console.

## Analyzing Number Frequency

The `number_frequency.py` script generates charts and trends based on historical data.

```bash
python3 analysis/number_frequency.py
```

* Generates frequency charts, heatmaps, and trends over time.
* Output charts are saved in the `charts/` directory.
* Uses `latest.csv` as the source data.

## Generating Fun Powerball Picks

The `powerball_picker.py` script generates number picks based on historical data and position-specific trends.

### Usage

```bash
python3 scripts/powerball_picker.py --picks 3 --strategy mixed
```

* `--picks` specifies the number of picks to generate.
* `--strategy` can be `hot`, `cold`, or `mixed`:

  * `hot`: favors frequently drawn numbers
  * `cold`: favors rarely drawn numbers
  * `mixed`: combination of hot and cold weighting

### Features

* Position-specific weighting for white balls (numbers are chosen based on historical appearance in each position).
* Avoids generating previously drawn combinations from `latest.csv`.
* Color-coded output for easy reading:

  * Hot numbers appear in **green**
  * Cold numbers appear in **red**
* Bulleted explanations for why each number was selected.

### Example Output

```
Generated 2 Powerball pick(s) using 'mixed' strategy:

Pick 1: Whites: 5, 12, 23, 34, 65 | Powerball: 19
  Reasons:
    • 5 (hot in white_1)
    • 12 (cold in white_2)
    • 23 (hot in white_3)
    • 34 (hot in white_4)
    • 65 (cold in white_5)
    • Powerball: 19 (hot)

Pick 2: Whites: 3, 17, 28, 42, 66 | Powerball: 11
  Reasons:
    • 3 (cold in white_1)
    • 17 (hot in white_2)
    • 28 (cold in white_3)
    • 42 (hot in white_4)
    • 66 (hot in white_5)
    • Powerball: 11 (cold)

Have fun and good luck! 🍀
```

## Notes

* This project is for educational and entertainment purposes.
* Lottery draws are random; the generated picks are fun, data-informed suggestions and not predictions.
