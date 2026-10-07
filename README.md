# ImagineArt Checkout & Cancellation Clarity — A Product Case Study

**TL;DR:** I analyzed 100 real, public customer reviews of ImagineArt (a generative-AI creative platform) and found that over half of all negative reviews — 53.3% — come down to one fixable problem: people don't understand what they're being charged, or how to cancel. This repo contains the full analysis, the product requirements document (PRD) for a fix, a proposed A/B test to validate it, and all the code used to collect and analyze the data.

> This is an independent, self-directed practice project. It is **not affiliated with ImagineArt or its parent company, Vyro**. I built it to practice real product-management methodology — the same process a product or growth team would use — on real, publicly available data.

---

## Why I built this

I'm applying for Associate Product Manager / Growth roles, and I wanted to show, not just claim, that I can do the actual job: find a real problem using real evidence, write a clear hypothesis, define success metrics, and design a way to test it — the same loop described in the "What You'll Do" sections of these job postings.

Rather than use a textbook dataset, I picked a real company's real public customer feedback and worked through it exactly as I'd do on the job.

---

## The headline finding

Of 100 scraped reviews, 60 were negative or neutral (3 stars or below). I read every single one and manually categorized it (a keyword script made a first guess; I corrected every row by hand). The result:

![Complaint categories chart](chart_complaint_categories_FINAL.png)

**53.3% of negative reviews (32 of 60) are billing or cancellation complaints** — more than triple the next-largest category (Output Quality, Credit Value, and Deceptive Search, each at 8.3%).

Digging further, those 32 complaints split into five distinct sub-problems — some fixable by a product/UX change, some needing a policy or legal owner instead. The full breakdown is in [`problem_and_hypothesis.md`](./problem_and_hypothesis.md).

---

## How I got there (the real process)

1. **Collected real data.** Scraped 100 live reviews from ImagineArt's public Trustpilot page using Python (`requests` + `BeautifulSoup`). When Trustpilot's bot-protection blocked automated requests, I used a fallback method — saving pages manually and parsing them with the same logic — and documented that limitation openly rather than hiding it.
2. **Categorized every review by hand.** A keyword-based script made a first-pass guess at each review's category; I then read all 100 myself and corrected every row, including several the script got wrong.
3. **Found the pattern, checked it against a competitor.** Billing/Refund was the dominant category. I compared ImagineArt's refund policy to a direct competitor's (OpenArt) and found ImagineArt's policy is actually *more* generous — which ruled out "loosen the policy" as the fix and pointed to **clarity**, not leniency, as the real problem.
4. **Wrote a hypothesis** — a specific, falsifiable prediction, not a vague feeling — and scoped it honestly to only the parts of the problem a product fix can actually solve.
5. **Wrote a full PRD**: problem, goals, success metrics (including guardrails, so the fix can't be judged a "win" if it quietly hurts something else), user stories, and an explicit list of open questions and dependencies I'd need to resolve with a real team before this could ship.
6. **Designed a proposed A/B test**, including the real statistics (required sample size, significance testing) — clearly labeled as a *design*, not a result, since I don't have access to ImagineArt's production systems.
7. **Sketched the actual fix** as a simple before/after mockup.
8. **Mapped the wider growth funnel** (acquisition, activation, retention, referral), honestly rating how strong the evidence was for each stage — rather than presenting every idea with false confidence.
9. **Ran one real, live growth experiment**: two different LinkedIn post styles promoting this project, to practice the "test content and messaging" side of a growth role with an actual measured result.

---

## Repository structure

```
├── README.md                         <- you are here
├── problem_and_hypothesis.md         <- the evidence, the 5 sub-patterns, the hypothesis, competitive check
├── PRD.md                            <- the full product requirements document
├── experiment_design.md              <- proposed A/B test: metrics, sample size, decision framework
├── funnel_opportunity_map.md         <- acquisition/activation/retention/referral opportunities, evidence-graded
├── mockup_before_after.png           <- sketch of the proposed checkout & cancellation screens
├── chart_complaint_categories_FINAL.png
├── categorized_reviews_FINAL.csv     <- the real, hand-corrected dataset behind every number in this project
├── linkedin_experiment/
│   ├── post_variants.md              <- the two real post drafts used for the content experiment
│   └── experiment_tracker.csv        <- real experiment log (hypothesis, metric, status, result)
├── code/
│   ├── SETUP.md                      <- step-by-step setup guide (no coding experience assumed)
│   ├── 01_scrape_reviews.py          <- live scraper (requests + BeautifulSoup)
│   ├── 01b_parse_saved_html.py       <- fallback scraper for manually-saved pages
│   ├── 02_categorize_reviews.py      <- first-pass keyword categorizer
│   ├── 03_analyze_and_chart.py       <- turns categorized data into the chart + stats
│   └── 04_ab_test_sample_size.py     <- real sample-size & significance-test statistics
├── PRD.docx                          <- Word version of the PRD
└── problem_and_hypothesis.docx       <- Word version of the problem/hypothesis doc
```

**If you only read one file, read `PRD.md`.** It links out to everything else.

---

## For non-technical readers

You don't need to touch any code to understand this project. Start with:
1. The **headline finding** above (the chart).
2. [`problem_and_hypothesis.md`](./problem_and_hypothesis.md) — what the problem actually is, in plain English.
3. [`PRD.md`](./PRD.md) — what I'd propose doing about it.

## For technical readers

Everything in `code/` is runnable end-to-end on a fresh machine — see `code/SETUP.md` for exact setup steps, including what each Python library does and how to troubleshoot common first-run errors (missing dependencies, Trustpilot's bot protection, etc.).

---

## Tech stack

**Python** (`requests`, `beautifulsoup4`, `pandas`, `matplotlib`, `scipy`) for data collection, analysis, and statistics · **Markdown** for documentation · manual qualitative coding for categorization · **Git/GitHub** for version control.

---

## Honesty notes — what this project is, and isn't

- The review data is 100% real and independently verifiable — the dataset is included, and the source is a live, public URL.
- The A/B test in `experiment_design.md` is a **proposed design**, not a result. I do not have access to ImagineArt's production systems or user base, and the documents say so explicitly rather than implying otherwise.
- The competitive check used public policy pages, not internal data.
- The LinkedIn experiment in `linkedin_experiment/` is the one part of this project with a real, measured result — everything else is analysis and design work, clearly labeled as such throughout.

I'd rather this project be smaller and entirely true than impressive and partly fabricated.

---

## Skills demonstrated

Real-world data collection (web scraping with a documented fallback plan) · qualitative coding and pattern-finding · competitive analysis · hypothesis writing · PRD authorship (problem, goals, guardrail metrics, user stories, scope, open questions) · A/B test design (sample size calculation, statistical significance) · growth-funnel analysis · running and measuring a real organic-content experiment.

---

## About

Built by **Mairaj Fatima** — BI Associate, data analyst, and aspiring Product Manager.
[GitHub](https://github.com/mairajfatima) · [LinkedIn](https://linkedin.com/in/mairaj-fatima-62207a310)

Feedback welcome — if you work in product, growth, or billing UX and see something I've missed, please open an issue.
