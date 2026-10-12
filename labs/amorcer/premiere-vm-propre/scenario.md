# Scenario: the shop's first machine

The course's common-thread shop has a costed architecture. It now needs its
first machine, the one that will carry the API. The team set itself three rules
before creating a single one:

1. **Nothing by hand.** Everything the machine carries at boot comes from a
   versioned user-data file. A machine you cannot recreate identically is a
   machine you will end up losing.
2. **No public address.** The machine is born on a private network. It can go
   out to fetch its packages; nobody can come in.
3. **Nothing survives the trial.** The test machine is destroyed at the end,
   with its network.

You start from a host where Incus works, a private network `lab-amorcer`
prepared by the lab, an SSH key pair and an incomplete user-data template.
No machine exists yet.
