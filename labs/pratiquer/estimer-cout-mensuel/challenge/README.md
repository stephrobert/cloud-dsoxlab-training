# Challenge: estimate a monthly cloud cost

Read `architecture.json` and create `cost-estimate.json` in the working
directory. Use the supplied dated price grid and monthly usage; do not fetch
live prices or infer an unlisted charge.

Record one line item per compute class, plus block storage, object storage,
snapshot storage, billable egress and API requests. Each line item must include
its ID, billed quantity, unit, unit price in EUR and monthly cost in EUR.
Also report the monthly total, annualized total, budget, remaining budget and
whether the estimate fits.

Use 730 hours for the standard month. Subtract the included egress allowance
before pricing outbound data. The exercise prices are synthetic, not provider
prices, and the result is an estimate rather than an invoice.

Run `dsoxlab check estimer-cout-mensuel` to see the result.
