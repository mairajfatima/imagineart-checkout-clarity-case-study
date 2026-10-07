"""
02_categorize_reviews.py

Takes raw_reviews.csv (from 01_scrape_reviews.py) and assigns each
review a first-pass category using keyword rules.

THIS IS A FIRST PASS, NOT THE FINAL ANSWER.
Keyword matching is fast but imprecise (e.g. a review that mentions
"credit" in passing isn't necessarily about credit value). After
running this script, open categorized_reviews.csv yourself and
correct any row where the auto-assigned category looks wrong. That
manual review step is the actual product-analyst skill being
demonstrated here — the script just gets you a fast starting point.

HOW TO RUN:
    python 02_categorize_reviews.py
"""

import csv

INPUT_FILE = "raw_reviews.csv"
OUTPUT_FILE = "categorized_reviews.csv"

# Order matters: a review is assigned to the FIRST category whose
# keywords it matches. Put more specific categories before general ones.
CATEGORY_RULES = [
    ("Deceptive Search", [
        "searching for", "thought i was", "google flow", "leonardo ai",
        "heygen", "believed i was signing up",
    ]),
    ("Billing/Refund", [
        "refund", "charged", "billing", "subscription", "cancel",
        "annual", "renewal", "chargeback", "trial",
    ]),
    ("Transparency", [
        "didn't know", "not clear", "hidden", "wasn't told", "misleading",
        "undisclosed", "draining", "leak",
    ]),
    ("Credit Value", [
        "credits ran out", "expensive", "credit cost", "waste of money",
        "value for money", "too many credits",
    ]),
    ("Output Quality", [
        "inconsistent", "quality", "did not match", "didn't match",
        "character consistency", "glitch", "bug", "doesn't work",
    ]),
    ("Onboarding/UX", [
        "confusing", "interface", "hard to find", "navigate", "cancel button",
        "delete account",
    ]),
    ("Feature Gap", [
        "wish it had", "missing feature", "doesn't support", "no way to",
        "character limit",
    ]),
    ("Positive", [
        "love it", "great", "excellent", "amazing", "best", "good quality",
        "highly recommend", "works great", "impressed",
    ]),
]


def categorize(title: str, text: str) -> str:
    combined = f"{title} {text}".lower()
    for category, keywords in CATEGORY_RULES:
        if any(kw in combined for kw in keywords):
            return category
    return "Uncategorized — needs manual review"


def main():
    rows = []
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["category_auto"] = categorize(row.get("title", ""), row.get("text", ""))
            row["category_final"] = ""  # you fill this in by hand after reviewing
            rows.append(row)

    fieldnames = list(rows[0].keys()) if rows else []
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Categorized {len(rows)} reviews -> {OUTPUT_FILE}")
    print("Now open the CSV and fill in 'category_final' for each row,")
    print("correcting any 'category_auto' value that looks wrong.")


if __name__ == "__main__":
    main()