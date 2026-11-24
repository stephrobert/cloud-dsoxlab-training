# A cloud access model before the first account is created

## The situation

The company is preparing its first production cloud environment. Teams share
an identity provider, several engineers need temporary production access, and
security must be able to reconstruct privileged activity. No cloud provider
has been selected, and the existing proposal relies on named users and
long-lived access keys.

A scenario says **where we are and what is wrong**, not the steps to take:
finding those is the learner's work.

The people, roles and audit constraints are described in `access-context.json`.
The design must also cover emergency access and the joiner, mover, leaver and
recertification lifecycle.

Skill targeted: `cloud.access.design`

## Design the access model

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
