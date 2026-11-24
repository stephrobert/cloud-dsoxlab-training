# The shop's first machine

## The situation

**Skill targeted: `cloud.environment.rebuild`.**

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

## Mission: the `boutique-vm1` machine

5 tasks, 100 points, 30 minutes

The work happens in `challenge/work`. The machine is created **from**
`challenge/work/user-data.yaml`: a machine configured by hand after it boots
does not count.

### Task 1: a VM on the private network, with no public address (20 pts)

An Incus **virtual machine** named `boutique-vm1`, running, plugged into the
`lab-amorcer` network only. All its global-scope addresses are in
`10.10.71.0/24`.

### Task 2: cloud-init finished, with your user-data (20 pts)

The instance's user-data is exactly `challenge/work/user-data.yaml`, which
starts with `#cloud-config` and carries no `???` any more. cloud-init returns
`status: done`, with no error.

### Task 3: the `boutique` user (20 pts)

Shell `/bin/bash`, password locked, not in the `sudo` group, and the key
`challenge/work/cle_lab.pub` authorised in its `authorized_keys`.

### Task 4: the packages (20 pts)

`jq` and `tree` are installed.

### Task 5: the role file (20 pts)

`/etc/boutique/role` contains `app`, belongs to `root:root`, mode `0644`.

## Check, then destroy

```bash
dsoxlab check amorcer-premiere-vm-propre
dsoxlab clean amorcer-premiere-vm-propre
```

Hints are available through `dsoxlab hint`, each deducted from the score: 10,
15 then 20 points.
