# Scenario: the same network, at another provider

The shop wants to keep an exit door: its private network must be declarable at
Outscale as well as at Scaleway. The need does not change: two zones, no public
address on the machines, a single controlled way out to the Internet. The model
does change: at Outscale, a subnet lives in a single Subregion, and the way out
goes through a NAT Service and route tables you link yourself.

The plan is settled (`PLAN.md`). You start from an empty emulator and the
`octl` CLI pointed at it. No resource exists yet.
