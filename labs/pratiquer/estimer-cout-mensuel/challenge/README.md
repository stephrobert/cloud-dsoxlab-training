# A monthly forecast before the architecture review

## The situation

The product team has proposed a small customer portal and asks whether its
cloud design fits a **400 EUR monthly resource budget**, excluding tax and
support. The architecture brief describes the expected monthly usage; a dated
exercise price grid is included in the supplied data.

Prepare a cost estimate that another reviewer can recalculate. Include the
compute, block and object storage, snapshots, API requests and outbound data
transfer in the brief. Distinguish usage from unit price, apply the included
egress allowance, and state the monthly total, annualized amount and budget
headroom.

The supplied grid is synthetic, not a provider quote. Feint and a cloud account
are not involved; the task is arithmetic and documented assumptions, not a
claim about a real invoice.

Skill targeted: `cloud.cost.estimate`

## Estimate a monthly cloud cost

Read `architecture.json` and create `cost-estimate.json` in the working
directory (`challenge/work/`). Use the supplied dated price grid and monthly usage; do not fetch
live prices or infer an unlisted charge.

Record one line item per compute class, plus block storage, object storage,
snapshot storage, billable egress and API requests. Each line item must include
its ID, billed quantity, unit, unit price in EUR and monthly cost in EUR.
Also report the monthly total, annualized total, budget, remaining budget and
whether the estimate fits.

Use 730 hours for the standard month. Subtract the included egress allowance
before pricing outbound data. The exercise prices are synthetic, not provider
prices, and the result is an estimate rather than an invoice.

Use this JSON shape (the values in angle brackets are yours to compute):

```json
{
  "currency": "<…>",
  "price_grid_as_of": "<…>",
  "line_items": [
    {"id": "<id>", "quantity": <…>, "unit": "<unit>", "unit_price_eur": <…>, "monthly_cost_eur": <…>}
  ],
  "total_monthly_eur": <…>,
  "annualized_eur": <…>,
  "monthly_budget_eur": <…>,
  "budget_remaining_eur": <…>,
  "within_budget": <true | false>
}
```

Line IDs and units: `compute-<class>` in `instance-hour` (one line per compute
class), `block-storage`, `object-storage` and `snapshot-storage` in
`GiB-month`, `egress` in `GiB`, `api-requests` in `million requests`.

Run `dsoxlab check estimer-cout-mensuel` to see the result.
