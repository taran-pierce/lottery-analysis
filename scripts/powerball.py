import argparse
import csv
import datetime
from pathlib import Path
import re
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from colorama import Fore, Style, init as colorama_init


# Initialize color output
colorama_init(autoreset=True)


BASE_URL = "https://www.coloradolottery.com/en/games/powerball/drawings/"


def fetch_page(url: str):
    """Fetch HTML content from a page."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_drawings(html):
    soup = BeautifulSoup(html, "html.parser")
    drawings = []

    drawing_blocks = soup.select("div.drawing")
    if not drawing_blocks:
        print("⚠️  No drawing blocks found.")
        return drawings

    for block in drawing_blocks:

        # --- Extract date ---
        date_tag = block.select_one("div.date a")
        if not date_tag:
            print("⚠️  Skipping block: no date found.")
            continue

        date_text = date_tag.get_text(strip=True)

        # --- Find the Powerball draw section ---
        powerball_draw = None
        for draw_div in block.select("div.draw"):
            title = draw_div.select_one("p.title")
            if title and "Powerball Numbers" in title.get_text():
                powerball_draw = draw_div
                break

        if not powerball_draw:
            print(f"⚠️  Skipping {date_text}: Powerball draw not found.")
            continue

        numbers_section = powerball_draw.select_one("div.numbers-and-jackpot")
        if not numbers_section:
            print(f"⚠️  Skipping {date_text}: no numbers-and-jackpot section.")
            continue

        # --- Extract white ball numbers ---
        white_section = numbers_section.select_one("p.draw")
        if not white_section:
            print(f"⚠️  Skipping {date_text}: no white ball section.")
            continue

        white_balls = [int(span.get_text(strip=True)) for span in white_section.select("span")]
        if len(white_balls) < 5:
            print(f"⚠️  Skipping {date_text}: not enough white balls ({white_balls}).")
            continue
        white_balls = white_balls[:5]

        # --- Extract Powerball number ---
        extra_section = numbers_section.select_one("p.extra span")
        if not extra_section:
            print(f"⚠️  Skipping {date_text}: missing Powerball (extra) number.")
            continue

        powerball = int(extra_section.get_text(strip=True))

        # --- Build dict ---
        drawing = {
            "date": date_text,
            "white_1": white_balls[0],
            "white_2": white_balls[1],
            "white_3": white_balls[2],
            "white_4": white_balls[3],
            "white_5": white_balls[4],
            "powerball": powerball,
        }

        drawings.append(drawing)

        # Console printout
        print(f"{date_text}: {white_balls} | PB {powerball}")

    return drawings



def print_results(draws):
    print("\n=== Parsed Powerball Drawings ===\n")

    for d in draws:
        white = [d["white_1"], d["white_2"], d["white_3"], d["white_4"], d["white_5"]]
        pb = d["powerball"]

        print(f"{d['date']}: {white} | PB {pb}")

    print(f"\nTotal Drawings Parsed: {len(draws)}\n")


def save_to_csv(draws, pages):
    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    os.makedirs(output_dir, exist_ok=True)

    # Auto filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"powerball_{pages}_pages_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)

    fieldnames = [
        "date",
        "white_1",
        "white_2",
        "white_3",
        "white_4",
        "white_5",
        "powerball",
    ]

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for d in draws:
            writer.writerow({
                "date": d["date"],
                "white_1": d["white_1"],
                "white_2": d["white_2"],
                "white_3": d["white_3"],
                "white_4": d["white_4"],
                "white_5": d["white_5"],
                "powerball": d["powerball"],
            })

    return filepath


def find_previous_page(soup):
    """Find the 'previous month' pagination link."""
    pages = soup.select_one(".pages")
    if not pages:
        return None

    prev_link = pages.find("a")
    if not prev_link:
        return None

    return prev_link["href"]


def scrape_pages(page_count):
    """Scrape a specified number of pages."""
    all_draws = []

    current_url = BASE_URL

    for _ in tqdm(range(page_count), desc="Scraping Pages", ncols=80):
        html = fetch_page(current_url)
        soup = BeautifulSoup(html, "html.parser")

        new_draws = parse_drawings(html)
        all_draws.extend(new_draws)

        prev_href = find_previous_page(soup)
        if not prev_href:
            break

        current_url = "https://www.coloradolottery.com" + prev_href

    return all_draws


def main():
    parser = argparse.ArgumentParser(
        description="Scrape Colorado Powerball lottery results."
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="Number of pages of results to scrape (default: 1)",
    )

    args = parser.parse_args()

    draws = scrape_pages(args.pages)

    print_results(draws)

    csv_path = save_to_csv(draws, args.pages)

    print(f"\n{Fore.GREEN}✔ Saved results to:{Style.RESET_ALL} {csv_path}")
    print(f"{Fore.GREEN}✔ Total drawings:{Style.RESET_ALL} {len(draws)}")


if __name__ == "__main__":
    main()
