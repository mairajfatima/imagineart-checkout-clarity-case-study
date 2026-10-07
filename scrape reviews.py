"""
01_scrape_reviews.py

Pulls real, public ImagineArt reviews from Trustpilot and saves them
to raw_reviews.csv (date, rating, title, text, url).

HOW TO RUN:
    pip install requests beautifulsoup4
    python 01_scrape_reviews.py

NOTES / HONESTY:
- This hits Trustpilot's PUBLIC review pages only (no login, no API key).
- Trustpilot may rate-limit or block automated requests. If you get
  empty results or a 403, that's their bot protection, not a bug in
  this script. Fallback options if that happens:
    1. Increase SLEEP_SECONDS below (be slower / more polite).
    2. Use a browser automation tool (Selenium/Playwright) instead
       of `requests`, since it renders like a real browser.
    3. Manually save the page HTML (Ctrl+S in your browser) and
       parse the local .html file with the same BeautifulSoup logic.
- This is for personal portfolio/research use on a small number of
  pages. Don't hammer the site with hundreds of rapid requests.
- Trustpilot's exact HTML attribute names can change over time.
  The selectors below (data-service-review-*) are Trustpilot's
  known review-card attributes as of 2026. If they've changed,
  open one review page in your browser, right-click a review ->
  Inspect, and update the selectors to match what you see.
"""

import time
import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.trustpilot.com/review/www.imagine.art"
NUM_PAGES = 6          # ~20 reviews per page -> ~120 reviews
SLEEP_SECONDS = 2       # be polite between requests
OUTPUT_FILE = "raw_reviews.csv"

HEADERS = {
    # A normal browser user-agent. Without this, many sites refuse the request outright.
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def parse_page(html: str, page_num: int) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    reviews = []

    # Trustpilot wraps each review in a card with this data attribute.
    cards = soup.find_all(attrs={"data-service-review-card-paper": True})

    for card in cards:
        # --- rating: an <img> or <div> with an aria-label like "Rated 5 out of 5 stars"
        rating = None
        rating_tag = card.find(attrs={"data-service-review-rating": True})
        if rating_tag and rating_tag.has_attr("data-service-review-rating"):
            rating = rating_tag["data-service-review-rating"]
        else:
            # fallback: look for an aria-label containing "Rated"
            img = card.find("img", alt=lambda a: a and "Rated" in a)
            if img:
                try:
                    rating = img["alt"].split("Rated")[1].split("out")[0].strip()
                except Exception:
                    rating = None

        # --- title
        title_tag = card.find(attrs={"data-service-review-title-typography": True})
        title = title_tag.get_text(strip=True) if title_tag else ""

        # --- body text
        text_tag = card.find(attrs={"data-service-review-text-typography": True})
        text = text_tag.get_text(strip=True) if text_tag else ""

        # --- date
        date_tag = card.find("time")
        date = date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else ""

        if title or text:
            reviews.append({
                "page": page_num,
                "date": date,
                "rating": rating,
                "title": title,
                "text": text,
            })

    return reviews


def main():
    all_reviews = []
    for page in range(1, NUM_PAGES + 1):
        url = BASE_URL if page == 1 else f"{BASE_URL}?page={page}"
        print(f"Fetching page {page}: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=15)

        if resp.status_code != 200:
            print(f"  -> Got status {resp.status_code}, stopping. "
                  f"(Likely bot protection — see notes at top of this file.)")
            break

        page_reviews = parse_page(resp.text, page)
        print(f"  -> Parsed {len(page_reviews)} reviews")
        all_reviews.extend(page_reviews)

        time.sleep(SLEEP_SECONDS)

    if not all_reviews:
        print("\nNo reviews parsed. Trustpilot likely blocked this request or "
              "changed their HTML. See the fallback options in the file header.")
        return

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["page", "date", "rating", "title", "text"])
        writer.writeheader()
        writer.writerows(all_reviews)

    print(f"\nSaved {len(all_reviews)} reviews to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()