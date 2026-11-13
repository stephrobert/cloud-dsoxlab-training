# Challenge: estimate a monthly cloud cost

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
