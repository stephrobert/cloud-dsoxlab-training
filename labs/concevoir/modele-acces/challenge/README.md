# Challenge: design the access model

Create `access-model.json` from the requirements in `access-context.json`.
Describe the human identity source and federation, session limit, emergency
accounts, role groups and permissions, separation of duties, lifecycle
ownership and audit-log requirements.

Your design must remain provider-neutral. Do not include real usernames,
credentials or provider-specific policy syntax.

The tests inspect the resulting design artifact. They do not prove that an
actual IAM service enforces it.

The JSON must include `human_identity`, `emergency_access`, `role_groups`,
`separation_of_duties`, `lifecycle` and `audit`. See the French challenge
README for a complete example shape.
