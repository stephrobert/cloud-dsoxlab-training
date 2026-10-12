# Mission: the `boutique-vm1` machine

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
