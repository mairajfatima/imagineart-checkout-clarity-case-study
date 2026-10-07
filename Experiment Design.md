# Experiment Design (Proposed)

> Labeled clearly: this test is **designed, not run**. I do not have access to ImagineArt's production systems or user base. This is the test I would propose running, written the way a real experiment plan is written.

## Design

| Item | Decision |
|---|---|
| Hypothesis | See `problem_and_hypothesis.md` |
| Unit of randomization | User, at first trial signup |
| Arms | **Control:** current checkout/cancellation flow. **Variant:** clear price/frequency line at checkout + separate "Cancel Subscription" button + trial-end reminder |
| Primary metric | Billing support tickets / refund requests per 1,000 active subscriptions |
| Guardrail metrics | Trial-to-paid conversion rate, involuntary churn rate |
| Baseline (assumed, needs real data to confirm) | Estimated from review volume — would need ImagineArt's actual ticket volume to calculate precisely |
| Significance / power | alpha = 0.05 (two-sided), power = 80% |
| Duration | Minimum one full billing cycle (30 days) to capture a full trial-to-conversion-to-cancellation cycle |

## Pre-launch checks (same discipline as any real test)

1. Sample-ratio-mismatch check once live.
2. QA the new checkout line and cancel button across web, iOS, and Android before launch — this is a billing-adjacent flow, so a bug here is costly.
3. Confirm event tracking fires correctly before trusting any results.

## Decision framework (set before results)

- **Ship:** billing tickets/refund requests down significantly, conversion guardrail holds.
- **Iterate:** tickets down but conversion drops more than 2pp — may need to soften the messaging, not remove it.
- **Don't ship:** no significant change in tickets — the real cause may lie elsewhere (e.g. pricing itself, not clarity).

## What I can't know without real access

The actual baseline ticket volume, true sample size needed, and whether 20% is a realistic target — these require ImagineArt's own data. I've written the design the way I'd defend it in an interview: the structure is real and correct; the specific numbers are placeholders pending real data.