# Cloud Training: practise without an account

**Language:** [English](./README.md) · [Français](./README.fr.md)

[![CI](https://github.com/stephrobert/cloud-dsoxlab-training/actions/workflows/ci.yml/badge.svg)](https://github.com/stephrobert/cloud-dsoxlab-training/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/stephrobert/cloud-dsoxlab-training?label=OpenSSF%20Scorecard)](https://securityscorecards.dev/viewer/?uri=github.com/stephrobert/cloud-dsoxlab-training)
[![Plumber compliance](https://score.getplumber.io/github.com/stephrobert/cloud-dsoxlab-training.svg)](https://score.getplumber.io/github.com/stephrobert/cloud-dsoxlab-training)
[![SLSA 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](./LICENSE)

Labs of the [Cloud course](https://blog.stephane-robert.info/docs/cloud/) (in
French) of blog.stephane-robert.info, driven by the
[`dsoxlab`](https://github.com/stephrobert/dsoxlab) CLI and played **without a
cloud account or a credit card**. The providers' official CLIs, `scw` for
Scaleway and `octl` for Outscale, drive **feint**, a local emulator of their
APIs; **Incus** boots the machines that must really start.

## What it is

`cloud-dsoxlab-training` is a **content repository**, not an application. It
provides:

- **guided labs** (level A of the course contract), which practise a move with
  the commands given;
- **challenges**, with no procedure and no free hint, which produce the proof
  of a skill;
- **automatic validation** that reads the **state** the learner leaves, in the
  emulator through the providers' public APIs, or in the machine through
  testinfra, never the commands typed;
- an **objectives grid**, the course's `cloud.*` skills: each lab names the one
  it tests;
- a **score** with hints of increasing cost.

## What feint proves, and what it does not

feint serves the **API contract** of Scaleway and Outscale: resources exist,
with their links, and read as they would at the provider. It forwards **no
packet**, applies neither routing nor NAT, and emulates neither prices, quotas
nor IAM. A network lab on feint therefore proves that an architecture is
**declared** correctly, not that traffic goes out. The lesson
[What feint proves](https://blog.stephane-robert.info/en/docs/cloud/outils/feint/limites/)
details it, and every lab concerned recalls it in its brief.

## Prerequisites

- Python 3.11+ and [`uv`](https://docs.astral.sh/uv/), `git`.
- **A working Docker** (`docker info`): feint runs in a container, image
  pinned by digest, started and stopped by dsoxlab. Port **4599** must be
  free.
- **[`mise`](https://mise.jdx.dev/)**, which installs feint, `scw` and `octl` at
  the versions in `mise.toml` (`mise install`).
- For the "A first clean VM" lab only: **Incus** usable without sudo, on a host
  able to virtualise
  ([install Incus](https://blog.stephane-robert.info/en/docs/incus/installation/)).

## Installation

```bash
# 1. Install the dsoxlab CLI (external tool, outside this repository)
uv tool install dsoxlab        # or: pipx install dsoxlab

# 2. Clone this lab catalog, and install its tools
git clone https://github.com/stephrobert/cloud-dsoxlab-training.git
cd cloud-dsoxlab-training
mise install

# 3. Check that the contract is valid
dsoxlab validate-structure
```

### Your first lab, in five minutes

```bash
dsoxlab list-labs                            # browse the catalog
dsoxlab run       reseau-prive-scaleway      # start feint, lay down the starting state
dsoxlab challenge reseau-prive-scaleway      # read the mission
cd labs/reseau/prive-scaleway/challenge/work
source feint-scaleway.env                    # point scw at the emulator
# ... you build the network with scw ...
dsoxlab check     reseau-prive-scaleway      # check and grade
dsoxlab clean     reseau-prive-scaleway      # stop feint, remove everything
```

One feint lab at a time: the labs share the same service, which `run` resets.
Stuck? `dsoxlab hint <id>` reveals a hint, whose cost is deducted from the
score.

### Keeping up to date

```bash
git pull                       # the catalog
uv tool upgrade dsoxlab        # the engine
mise install                   # the pinned tools
```

A lab that fails after an upgrade of feint, `scw` or `octl` is a defect of the
catalog: open an issue, the form comes pre-filled by `dsoxlab support --issue`.

## How it works

### The declarative contract, on two levels

- **`meta.yml`**, at the root, declares the repository's identity, the
  **order** of the labs, that of the blog's path, and reserves the catalog's
  network (`lab-cloud`, `10.10.70.0/24`) for the machine labs to come;
- **`lab.yaml`**, per lab, declares its `skills`, its `level`, its `runtime`
  (type, fixtures, **services**), its `doc_url` and a `validation` block. A
  `lab.fr.yaml` overrides the `title` and the `description` in French.

### Runtimes

| Runtime | What the lab requires |
|---|---|
| `shell` + feint service | a terminal, Docker and the CLIs of `mise.toml`. dsoxlab starts feint, the `setup.yaml` resets it (and, for a challenge, declares in it the environment to read). |
| `shell` + Incus | a terminal and Incus. The `setup.yaml` prepares a dedicated private network; the learner boots the machine there; `clean` destroys it with its network. |

### The validation model

Validation **proves the state, it does not trust the learner**. The tests read
feint through the public APIs of Scaleway and Outscale, or enter the machine
through `incus exec` and testinfra. A challenge drawn at random stores its
reference inventory **outside** the working directory, to refuse a modified
environment.

A lab is tested **both ways**: the tests must fail before the work and pass
after it. `scripts/valider-labs.py` records it through the real dsoxlab
commands in `validation-labs.json`; `scripts/verify-solutions.py --deux-sens`
does it again **without dsoxlab**, starting feint itself and playing
`setup.yaml`: removing the tool must leave the labs playable.

Reference solutions live under `solution/`, **encrypted with ansible-vault**:
a solution shipped in clear text spoils the lab, and git keeps it forever.

### The objectives grid: the course's skills

Each scenario names the skill it tests: "Skill targeted:
`cloud.network.design`". `curriculums.yml` holds the course's 18 skills, and
`tests/test_curriculums.py` refuses an identifier missing from the grid, or an
announced skill that the `lab.yaml` does not carry.

### Links to the guides

A lab's `doc_url` is the French lesson, because dsoxlab reads it. The README
links are **computed**: `scripts/gen_doc_url_en.py` reads the site's
`translationOf`, and `scripts/gen_catalog.py` points the English README at the
translation when it exists.

## Catalog

<!-- LABS:START -->
### Practise without an account

| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pratiquer-challenge-budget-contraint` | Challenge 1: an architecture on a tight budget | a | shell | [guide](https://blog.stephane-robert.info/en/docs/cloud/outils/feint/limites/) |

### Boot a machine

| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `amorcer-premiere-vm-propre` | A first clean VM: booted by cloud-init, with no public address | a | shell | [guide (FR)](https://blog.stephane-robert.info/docs/cloud/cloud-init/) |

### Cloud networking

| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `reseau-prive-scaleway` | Private network, and first instances with no public address: scw on Feint | a | shell | [guide (FR)](https://blog.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/) |
| `reseau-prive-outscale` | Private network, and first instances with no public address: octl on Feint | a | shell | [guide (FR)](https://blog.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/) |

_4 labs, table generated by `scripts/gen_catalog.py`._
<!-- LABS:END -->

## Contributing and license

Contributions are welcome: read [CONTRIBUTING.md](./CONTRIBUTING.md), which
describes the anatomy of a lab of this repository and the golden rule, a lab is
tested both ways. The [code of conduct](./CODE_OF_CONDUCT.md) applies to every
exchange, and vulnerabilities are reported privately: [SECURITY.md](./SECURITY.md).

### License

This content is published under [Creative Commons Attribution 4.0
International](./LICENSE) (CC BY 4.0). You may share and adapt it, including
commercially, provided you credit the source.
