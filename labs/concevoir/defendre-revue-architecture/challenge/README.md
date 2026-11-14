# Challenge: defend the architecture review

Read `review-evidence.json` and write two files in the working directory (`challenge/work/`):

- `review.json` with the six scores, cited evidence, three highest risks, ADR
  decisions, owners, due dates and evidence limits;
- `review.md`, a concise report for the architecture board.

Score each of the six axes (`operational-excellence`, `security`,
`reliability`, `performance`, `cost`, `sovereignty`) from 0 to 3 with this grid,
from the kind and content of its evidence:

| Score | The evidence of the axis |
|---|---|
| 3 | a verified, dated test or measurement shows the requirement met |
| 2 | a configuration or an estimate shows the requirement met, without verification |
| 1 | shows the requirement unmet, or not assessed |
| 0 | there is none |

The `risks` in the evidence pack are ordered by severity multiplied by
likelihood. Select the three highest, and for each record a decision
(`correct`, `accept` or `defer`), a reason, an owner, a due date and an action.
An accepted risk must name the person accountable for accepting it.

State all supplied `evidence_limits`; do not claim that this exercise proves a
live provider bill, IAM enforcement or dataplane behavior.

Run `dsoxlab check defendre-revue-architecture` to see the result.
