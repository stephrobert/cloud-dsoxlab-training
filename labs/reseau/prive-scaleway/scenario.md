# Scenario: the shop's private network

**Skill targeted: `cloud.network.design`.**

The shop has its first machine booted locally. Before declaring a single
instance at a provider, the team sets a rule: **nothing exposed before the
private network**. The API and its front end will run in two zones of the
`fr-par` region, with no public address, and go out for their updates through
a single gateway.

The address plan is settled (`PLAN.md`). It remains to declare it at Scaleway,
and to prove it through the state, before the first credit card comes into
play: that is the role of feint, which serves the same API with no account.

You start from an empty emulator, the `scw` CLI installed and the environment
that points it at the emulator. No resource exists yet.
