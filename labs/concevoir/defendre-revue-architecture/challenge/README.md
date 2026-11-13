# Challenge: defend the architecture review

Read `review-evidence.json` and write two files in the working directory:

- `review.json` with the six scores, cited evidence, three highest risks, ADR
  decisions, owners, due dates and evidence limits;
- `review.md`, a concise report for the architecture board.

Use scores from 0 to 3. A score of 3 requires a dated test or measurement;
configuration or estimates alone cannot receive 3. The six axes are:
`operational-excellence`, `security`, `reliability`, `performance`, `cost` and
`sovereignty`.

The `risks` in the evidence pack are ordered by severity multiplied by
likelihood. Select the three highest, and for each record a decision
(`correct`, `accept` or `defer`), a reason, an owner, a due date and an action.
An accepted risk must name the person accountable for accepting it.

State all supplied `evidence_limits`; do not claim that this exercise proves a
live provider bill, IAM enforcement or dataplane behavior.

Run `dsoxlab check defendre-revue-architecture` to see the result.
