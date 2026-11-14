# Scenario: a cloud access model before the first account is created

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
