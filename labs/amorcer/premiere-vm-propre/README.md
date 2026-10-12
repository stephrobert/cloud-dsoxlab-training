# A first clean VM: booted by cloud-init, with no public address

A well-born cloud machine is not configured by hand after it boots: at boot it
receives a **user-data** file that **cloud-init** applies once, and it is born
on a **private network**, with no address reachable from the Internet. This lab
has you make that move locally, without a cloud account: an **Incus** virtual
machine plays the instance, a private Incus network plays the provider's
network.

Lesson of the site that carries this lab (in French):
<https://blog.stephane-robert.info/docs/cloud/cloud-init/>.

## What you will be able to do

- Write a valid user-data: a user with no password reachable by SSH key,
  packages installed at first boot, a file laid down with its permissions.
- Boot a virtual machine from that file alone, on a private network with
  outbound NAT.
- Check that cloud-init finished without error, and that the machine has no
  public address.
- Destroy the machine and what surrounds it, leaving nothing behind.

## Prerequisites

- **Incus installed and usable without sudo** (your account in the
  `incus-admin` group):
  <https://blog.stephane-robert.info/en/docs/incus/installation/>.
  The host must be able to virtualise (KVM): `incus info | grep -i virtual`
  must name `qemu`.
- **dsoxlab installed**:
  <https://blog.stephane-robert.info/en/docs/dsoxlab/installation/>.
- Outbound Internet access: the image (about 300 MB on first pull) and the
  packages are downloaded.

## Duration

About 30 minutes, including one minute of machine boot once the image is
cached.

## What `dsoxlab run` prepares

- the private network `lab-amorcer`: `10.10.71.0/24`, outbound NAT, no IPv6;
- an SSH key pair for the lab, `cle_lab` and `cle_lab.pub`, in
  `challenge/work`;
- a template `challenge/work/user-data.yaml`, with `???` holes.

```bash
dsoxlab run amorcer-premiere-vm-propre
cd labs/amorcer/premiere-vm-propre/challenge/work
```

## Step 1: write the user-data

The file starts **exactly** with `#cloud-config`: without that line,
cloud-init ignores everything else, with no visible error. Fill the template to
get:

```yaml
#cloud-config
users:
  - name: boutique
    shell: /bin/bash
    lock_passwd: true
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... boutique-lab   # the content of cle_lab.pub
package_update: true
packages:
  - jq
  - tree
write_files:
  - path: /etc/boutique/role
    content: |
      app
    owner: root:root
    permissions: "0644"
```

Three choices deserve a word. `lock_passwd: true` locks the password: the
account opens with the key only. The user is **not** in the `sudo` group: it is
an application account, not an administration account. The permissions
`"0644"` are **quoted**, otherwise YAML reads them as a decimal number.

## Step 2: boot the machine from the file

```bash
incus launch images:ubuntu/noble/cloud boutique-vm1 --vm \
  --network lab-amorcer \
  --config=cloud-init.user-data="$(cat user-data.yaml)"
```

`--vm` asks for a **virtual machine**, with its own kernel, like a cloud
instance. `--network lab-amorcer` plugs it into the private network only. The
user-data goes through the `cloud-init.user-data` key, as it goes through the
metadata service at a provider.

## Step 3: check from the machine

```bash
incus exec boutique-vm1 -- cloud-init status --wait
incus exec boutique-vm1 -- id boutique
incus exec boutique-vm1 -- dpkg-query -W jq tree
incus exec boutique-vm1 -- cat /etc/boutique/role
incus list boutique-vm1 -c n4t
```

`status: done` means cloud-init has finished. The address shown is in
`10.10.71.x`: private, reachable from your host, invisible from the Internet.
The machine still goes out to install its packages, through the network's
**NAT**, exactly as an instance with no public IP goes out through the NAT
gateway of its cloud network.

```bash
dsoxlab check amorcer-premiere-vm-propre
```

## Step 4: destroy

A forgotten machine keeps costing at a provider. Here the rule is the same:

```bash
dsoxlab clean amorcer-premiere-vm-propre
incus list boutique-vm1        # the list must be empty
```

`clean` destroys the machine, then the `lab-amorcer` network.

## What this lab does not prove

An Incus machine is not a provider instance: the metadata service, the images
and the real addressing differ. The move is the same: one file, one boot, no
manual step, no public address.
