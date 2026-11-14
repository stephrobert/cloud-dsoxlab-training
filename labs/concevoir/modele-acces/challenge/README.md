# Challenge: design the access model

Create `access-model.json` in `challenge/work/` from the requirements in `access-context.json`.
Describe the human identity source and federation, session limit, emergency
accounts, role groups and permissions, separation of duties, lifecycle
ownership and audit-log requirements.

Your design must remain provider-neutral. Do not include real usernames,
credentials or provider-specific policy syntax.

The tests inspect the resulting design artifact. They do not prove that an
actual IAM service enforces it.

The JSON must include `human_identity`, `emergency_access`, `role_groups`,
`separation_of_duties`, `lifecycle` and `audit`, in this shape (the values in
angle brackets are yours to derive from `access-context.json`):

```json
{
  "human_identity": {
    "source": "<…>",
    "federation_protocol": "<…>",
    "single_sign_on": <true | false>,
    "maximum_session_minutes": <…>
  },
  "emergency_access": {
    "accounts": [
      {"named_owner": "<…>", "mfa": <…>, "routine_use": <…>, "alert_on_use": <…>}
    ]
  },
  "role_groups": [
    {"name": "<…>", "duties": ["<…>"]}
  ],
  "separation_of_duties": {
    "approval_and_production_deployment_use_distinct_people": <…>,
    "production_access_is_temporary": <…>
  },
  "lifecycle": [
    {"event": "<…>", "owner": "<…>", "maximum_completion_hours": <…>, "interval_days": <… for a periodic event>}
  ],
  "audit": {
    "events": ["<…>"],
    "retention_days": <…>,
    "immutable_destination": <…>,
    "destination_owner": "<…>",
    "readers": ["<…>"],
    "alert_on": ["<…>"]
  }
}
```
