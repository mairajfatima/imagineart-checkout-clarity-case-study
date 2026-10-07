# PRD: Checkout Clarity & Self-Service Cancellation

> Independent product analysis based on real, public ImagineArt customer reviews (Trustpilot). Not affiliated with ImagineArt/Vyro. Problem, hypothesis and competitive check are in `problem_and_hypothesis.md`.

| | |
|---|---|
| **Author** | Mairaj Fatima |
| **Status** | Proposed, based on real review analysis |
| **Product area** | Billing / Account Management |

## 1. Problem (summary)

Real customer reviews show a recurring pattern: users are charged in ways they did not expect (trial converting to paid, monthly vs. annual confusion) and then cannot easily self-serve a cancellation, which pushes them to public complaints and chargebacks instead. 32 of 60 negative/neutral reviews in a 100-review scraped sample (53.3%) fall into this category — the single largest complaint cluster found, more than triple the next category. See `problem_and_hypothesis.md` for the five sub-patterns within it (A-E) and why this PRD scopes to only three of them (A, B, C).

## 2. Hypothesis

If checkout clearly shows total price and billing frequency before confirmation, and a one-click "Cancel Subscription" option exists separate from "Delete Account," billing complaints and refund requests will decrease. (Full reasoning in `problem_and_hypothesis.md`.)

## 3. Goals and success metrics

| Type | Metric | Target |
|---|---|---|
| **Primary** | Billing-related support tickets / refund requests per 1,000 active subscriptions | Reduce by 20% within 60 days of launch |
| Secondary | Trial-to-paid cancellation rate within the trial window | Increase (more users successfully self-cancel before being charged, rather than being charged and disputing after) |
| Guardrail | Overall trial-to-paid conversion rate | Should not drop more than 2pp — the goal is clarity, not discouraging legitimate conversions |
| Guardrail | Involuntary churn via chargebacks | Should decrease, not increase |

**Non-goals:** changing the refund policy itself, changing pricing, redesigning the full billing page beyond the two flows below. Also explicitly out of scope: refund-refusal/support-flexibility complaints (sub-pattern D) and "unlimited" marketing-claim disputes (sub-pattern E) — both need policy/legal owners, not a product fix, and are flagged separately rather than folded into this PRD.

## 4. Users

All free users entering a paid trial, and all active subscribers managing their plan.

## 5. Requirements

| # | User story | Priority |
|---|---|---|
| R1 | As a user starting a trial, I see the exact amount and date I'll be charged if I don't cancel, directly on the trial confirmation screen. | Must |
| R2 | As a user at checkout, I see the billing frequency (monthly/annual) and total price in a single, unmissable line before I confirm payment. | Must |
| R3 | As a subscriber, I can find and use a clearly labeled "Cancel Subscription" button in account settings, separate from "Delete Account." | Must |
| R4 | As a user who cancels, I receive an immediate on-screen and email confirmation showing the cancellation date and what happens to my access/credits. | Must |
| R5 | As a user approaching the end of a trial, I receive a reminder (in-app and email) 24 hours before conversion to paid. | Should |

**Out of scope:** refund policy changes, pricing changes, full account-settings redesign.

## 6. Tracking plan

Events: `trial_started`, `trial_reminder_shown`, `trial_converted_to_paid`, `checkout_price_viewed`, `checkout_confirmed`, `cancel_subscription_clicked`, `cancel_subscription_confirmed`, `billing_support_ticket_opened`. All carry `user_id`, `plan_type`, `platform`, `experiment_group`.

## 7. Risks

- **Risk:** clearer pricing/cancellation reduces trial-to-paid conversion. *Mitigation:* conversion rate is a guardrail metric.
- **Risk:** engineering cost of two new UI surfaces (checkout line, cancel button) within timeline. *Mitigation:* R1-R4 are "Must," R5 is "Should" and can slip.

See `experiment_design.md` for how this would be tested.

## 8. Open questions & dependencies

These are genuinely unresolved — things I don't have access to answer from public review data alone, and would need to find out from the real team before this PRD could move past a first draft.

**Open questions:**
1. **Does the existing "Delete Account" flow already cancel billing, or does it leave the subscription active?** Reviews are inconsistent on this — some describe being charged *after* deleting their account, others don't mention it. This changes whether R3 is a new feature or a fix to a broken one, and I can't tell which from the outside.
2. **What's the actual current billing-ticket volume?** `experiment_design.md` assumes a 3% baseline rate to calculate sample size — that number is a placeholder, not real. Without it, I can't say whether 11,452 users/arm is actually achievable in a reasonable timeframe for ImagineArt's real traffic.
3. **Who owns this problem — Product, Growth, or Support/Billing?** The fix touches checkout (Product/Eng), cancellation flow (Product/Eng), and refund policy enforcement (Support/Legal, out of scope here). A real PRD would need this named before requirements get assigned.
4. **Is "unlimited" language (sub-pattern E) a marketing/legal issue, not just a product one?** If "unlimited" plans have undisclosed caps, that's potentially a deceptive-advertising exposure, not only a UX problem — I flagged it as out of scope for this PRD, but it likely needs its own owner urgently, possibly before this one.

**Dependencies:**
1. **Payment provider capability.** R1/R2 (showing exact price/frequency before confirmation) depends on whatever payment processor ImagineArt uses (Stripe, Paddle, or similar) supporting that display without a full checkout rebuild. I don't know which provider they use, so I can't say how large this engineering lift actually is.
2. **Mobile platform constraints.** If subscriptions on iOS go through Apple's in-app purchase system, Apple — not ImagineArt — controls the cancellation flow and UI; Apple's own subscription-management screen would be the "Cancel Subscription" surface on iOS, not a custom one ImagineArt builds. R3 may only be fully buildable on web, with iOS/Android needing a different approach (e.g., deep-linking to the platform's native subscription settings). This matters a lot for scoping and I didn't have it fully worked out in the original requirements.
3. **Regulatory context.** Several markets now have specific rules about cancellation ease for recurring subscriptions (e.g., the US FTC's "click-to-cancel" rule, and similar consumer-protection rules in the EU). I haven't checked whether these apply to ImagineArt's user base, but if they do, R3 may not be optional — it could be a compliance requirement, which would change this PRD's priority entirely.