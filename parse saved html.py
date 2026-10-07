"""
01b_parse_saved_html.py

FALLBACK for 01_scrape_reviews.py, for when Trustpilot blocks automated
requests (a 403 error). Instead of downloading pages automatically, this
reads HTML files YOU saved manually from your own browser.

HOW TO GET THE INPUT FILES (do this first, in your browser):
  1. Open https://www.trustpilot.com/review/www.imagine.art
  2. Press Ctrl+S, save as type "Webpage, HTML only", name it page1.html,
     save it in this same project folder.
  3. Go to https://www.trustpilot.com/review/www.imagine.art?page=2
     Ctrl+S -> save as page2.html, same folder.
  4. Repeat for page=3, page=4, page=5 -> page3.html, page4.html, page5.html

HOW TO RUN:
    pip install beautifulsoup4
    python 01b_parse_saved_html.py
"""

import csv
import glob
from bs4 import BeautifulSoup

OUTPUT_FILE = "raw_reviews.csv"


def parse_file(path: str, page_num: int) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    reviews = []
    cards = soup.find_all(attrs={"data-service-review-card-paper": True})

    for card in cards:
        rating = None
        rating_tag = card.find(attrs={"data-service-review-rating": True})
        if rating_tag and rating_tag.has_attr("data-service-review-rating"):
            rating = rating_tag["data-service-review-rating"]
        else:
            img = card.find("img", alt=lambda a: a and "Rated" in a)
            if img:
                try:
                    rating = img["alt"].split("Rated")[1].split("out")[0].strip()
                except Exception:
                    rating = None

        title_tag = card.find(attrs={"data-service-review-title-typography": True})
        title = title_tag.get_text(strip=True) if title_tag else ""

        text_tag = card.find(attrs={"data-service-review-text-typography": True})
        text = text_tag.get_text(strip=True) if text_tag else ""

        date_tag = card.find("time")
        date = date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else ""

        if title or text:
            reviews.append({
                "page": page_num, "date": date, "rating": rating,
                "title": title, "text": text,
            })

    return reviews


def main():
    files = sorted(glob.glob("page*.html"))
    if not files:
        print("No page*.html files found in this folder.")
        print("Did you save them yet? See the instructions at the top of this file.")
        return

    all_reviews = []
    for i, path in enumerate(files, start=1):
        print(f"Reading {path}...")
        page_reviews = parse_file(path, i)
        print(f"  -> Parsed {len(page_reviews)} reviews")
        all_reviews.extend(page_reviews)

    if not all_reviews:
        print("\nParsed 0 reviews from the saved files.")
        print("This usually means Trustpilot's HTML structure uses different")
        print("attribute names than expected. Send me a review of the saved")
        print("page1.html and I'll help you find the right selectors.")
        return

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["page", "date", "rating", "title", "text"])
        writer.writeheader()
        writer.writerows(all_reviews)

    print(f"\nSaved {len(all_reviews)} reviews to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()