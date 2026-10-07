# Problem Definition, Hypothesis & Competitive Check

> Based on **100 real Trustpilot reviews of ImagineArt** (imagine.art), scraped and hand-coded by me. Source: trustpilot.com/review/www.imagine.art

## Step 2: The problem, defined precisely

Of 100 reviews scraped, 60 were negative or neutral (rating ≤ 3 stars). Of those 60, **32 (53.3%) were Billing/Refund complaints — the single largest category by a wide margin**, more than triple the next-largest category (Credit Value, Deceptive Search, and Output Quality each at 5 reviews / 8.3%).

Reading all 32 Billing/Refund reviews closely, the complaints cluster into **five distinct sub-patterns**, not one:

| Sub-problem | Count (of 32) | Example pattern |
|---|---|---|
| **A. Trial-to-paid conversion surprises users** | 3 | Low-cost trial (e.g. $2) converts to a full charge; user believed they had cancelled in time |
| **B. Monthly vs. annual billing isn't clear at checkout** | 5 | User believes they selected monthly, is charged the annual total (one case: $492) |
| **C. No clear self-service cancellation path** | 7 | No visible "Cancel Subscription" option; users describe it as deliberately difficult to find |
| **D. Refund refused / rigid policy / value mismatch** | 13 | Refund requests denied even within the stated window; several describe support as unhelpful or the policy as deliberately restrictive |
| **E. Misleading "unlimited" generation claims** | 4 | "Unlimited" plans turn out to be time-limited (e.g. disappearing after one day) or model-limited, discovered only after paying |

**The precise problem:** this isn't one problem, it's a cluster of related ones, and sub-pattern E is a notable finding — "unlimited" marketing claims that aren't actually unlimited appear repeatedly enough (4 of 32) to be a distinct, specific risk, separate from the checkout-clarity issue in A/B/C. A single PRD should scope tightly around A, B and C (the parts a product/UX fix can directly address); D and E likely need separate owners (policy/support for D, marketing/legal review for E) and are flagged as out of scope for this PRD rather than folded in.

## Step 3: Hypothesis

> **If** the checkout flow clearly displays the total price and billing frequency before payment is confirmed, and the account settings include a one-click "Cancel Subscription" option (distinct from "Delete Account"), **then** billing-related complaints and refund requests tied to sub-patterns A, B and C will decrease, **because** the harm in those three sub-patterns happens *before* the user ever needs a refund — fixing visibility at checkout and cancellation prevents the complaint from being created in the first place, rather than resolving it after the fact.

This is a **prevention-first** hypothesis, deliberately scoped to the 15 of 32 billing reviews (A+B+C) that a checkout/cancellation fix can actually address — not all 32, since D and E need different fixes entirely. Being explicit about what this hypothesis does *not* claim to fix is itself part of writing it correctly.

## Step 4: Competitive check (real data)

| Company | Refund policy | What their own users complain about |
|---|---|---|
| **ImagineArt** | 3-5 day window, under 300 credits used | Trial-to-paid surprises, unclear monthly/annual selection, no self-service cancel, "unlimited" claims disputed |
| **OpenArt** | Strict no-refund policy (no exceptions in public terms) | Same complaint *shape*: accidental annual renewals, unused credits wiped on renewal, difficulty cancelling |

**Key finding:** ImagineArt's refund policy is actually **more generous** than OpenArt's blanket no-refund stance, yet both draw a similar volume and shape of complaint. This rules out "loosen the refund policy" as the fix and points to checkout/cancellation **clarity** — supporting the hypothesis above.