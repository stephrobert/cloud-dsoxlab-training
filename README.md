# Cloud Training: practise without an account

**Language:** [English](./README.md) · [Français](./README.fr.md)

[![CI](https://github.com/stephrobert/cloud-dsoxlab-training/actions/workflows/ci.yml/badge.svg)](https://github.com/stephrobert/cloud-dsoxlab-training/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/stephrobert/cloud-dsoxlab-training?label=OpenSSF%20Scorecard)](https://securityscorecards.dev/viewer/?uri=github.com/stephrobert/cloud-dsoxlab-training)
[![Plumber compliance](https://score.getplumber.io/github.com/stephrobert/cloud-dsoxlab-training.svg)](https://score.getplumber.io/github.com/stephrobert/cloud-dsoxlab-training)
[![SLSA 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](./LICENSE)

Labs of the [Cloud course](https://www.stephane-robert.info/docs/cloud/) (in
French) of www.stephane-robert.info, driven by the
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
[What feint proves](https://www.stephane-robert.info/en/docs/cloud/outils/feint/limites/)
details it, and every lab concerned recalls it in its brief.

## Requirements

- Python 3.11+ and [`uv`](https://docs.astral.sh/uv/), `git`.
- **A working Docker** (`docker info`): feint runs in a container, image
  pinned by digest, started and stopped by dsoxlab. Port **4599** must be
  free.
- **[`mise`](https://mise.jdx.dev/)**, which installs feint, `scw` and `octl` at
  the versions in `mise.toml` (`mise install`).
- For the "A first clean VM" lab only: **Incus** usable without sudo, on a host
  able to virtualise
  ([install Incus](https://www.stephane-robert.info/en/docs/incus/installation/)).

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

### The lab lifecycle

```bash
dsoxlab list-labs              # browse the catalog
dsoxlab show      <id>         # metadata and status of one lab
dsoxlab run       <id>         # set the starting state
dsoxlab challenge <id>         # read the mission, no step-by-step
dsoxlab hint      <id>         # reveal a hint (deducted from the score)
dsoxlab check     <id>         # run the tests, compute and record the score
dsoxlab clean     <id>         # remove the work directory and stop the services
dsoxlab progress               # per-section progress, average score
```

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

### Scoring, hints, progress

`check` records a score (tests passed out of total, minus the cost of any hints
revealed). Hints are **base64-encoded** in `challenge/hints.yaml`, so that
opening the file does not give them away, and their cost grows with their
precision. History lives in a SQLite database **local to this repository**.

A run that measured nothing is neither a pass nor a failure: if every collected
test skips, `check` records no score and says why. This catalog is where that
defect was found: a challenge whose feint service was down reported five
skipped tests as a pass, and recorded a 0 for a lab nobody had played.

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

Module 2b: official CLIs plugged into feint, a budget challenge, and design exercises for cost, data services and elasticity.

5 lab(s).

| # | Lab | Title | Skill | Duration | Validated | Companion guide |
|---|---|---|---|---|---|---|
| 1 | [`pratiquer-challenge-budget-contraint`](labs/pratiquer/challenge-budget-contraint/) | Challenge 1: an architecture on a tight budget | cloud.cost.estimate | 45m | validated | [guide](https://www.stephane-robert.info/en/docs/cloud/outils/feint/limites/) |
| 2 | [`estimer-cout-mensuel`](labs/pratiquer/estimer-cout-mensuel/) | Estimate a cloud architecture's monthly cost | cloud.cost.estimate | 30m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/fondamentaux/pay-as-you-go-modeles-tarifaires/) |
| 3 | [`choisir-service-donnees`](labs/pratiquer/choisir-service-donnees/) | Choose a managed data service | cloud.data.choose | 35m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/donnees/) |
| 4 | [`concevoir-elasticite`](labs/pratiquer/concevoir-elasticite/) | Design an elastic application tier | cloud.elasticity.design | 35m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/fondamentaux/elasticite-vs-scalabilite/) |
| 5 | [`pratiquer-choisir-modele-cloud`](labs/pratiquer/choisir-modele-cloud/) | Choose a cloud service and deployment model | cloud.model.choose | 30m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/fondamentaux/modeles-cloud-iaas-paas-saas/) |

### Boot a machine

Module 2c: a first virtual machine booted by cloud-init, with no public address, then destroyed.

1 lab(s).

| # | Lab | Title | Skill | Duration | Validated | Companion guide |
|---|---|---|---|---|---|---|
| 1 | [`amorcer-premiere-vm-propre`](labs/amorcer/premiere-vm-propre/) | A first clean VM: booted by cloud-init, with no public address | cloud.environment.rebuild | 30m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/cloud-init/) |

### Cloud networking

Module 3: a regional private network attached in two zones, an egress gateway and its default route, declared on feint.

2 lab(s).

| # | Lab | Title | Skill | Duration | Validated | Companion guide |
|---|---|---|---|---|---|---|
| 1 | [`reseau-prive-scaleway`](labs/reseau/prive-scaleway/) | Private network, and first instances with no public address: scw on Feint | cloud.network.design | 40m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/) |
| 2 | [`reseau-prive-outscale`](labs/reseau/prive-outscale/) | Private network, and first instances with no public address: octl on Feint | cloud.network.design | 45m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/) |

### Cloud architecture decisions

Choose and size compute, design identity and access, decide on architecture options, prioritize improvements, and defend an evidence-based review.

5 lab(s).

| # | Lab | Title | Skill | Duration | Validated | Companion guide |
|---|---|---|---|---|---|---|
| 1 | [`concevoir-architecture-cible`](labs/concevoir/architecture-cible/) | Decide on a target cloud architecture | cloud.architecture.decide | 40m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/capstone/decider-une-architecture-cible/) |
| 2 | [`concevoir-modele-acces`](labs/concevoir/modele-acces/) | Design a cloud identity and access model | cloud.access.design | 40m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/securite/iam/) |
| 3 | [`concevoir-recommander-evolutions-architecture`](labs/concevoir/recommander-evolutions-architecture/) | Turn architecture findings into a prioritised action plan | cloud.architecture.recommend | 40m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/capstone/recommander-des-evolutions/) |
| 4 | [`defendre-revue-architecture`](labs/concevoir/defendre-revue-architecture/) | Defend a cloud architecture review with evidence | cloud.architecture.review | 45m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/fondamentaux/well-architected-frameworks/) |
| 5 | [`choisir-modele-calcul`](labs/concevoir/choisir-modele-calcul/) | Choose a compute model and size it from measurements | cloud.compute.choose | 35m | validated | [guide (FR)](https://www.stephane-robert.info/docs/cloud/compute/machines-et-dimensionnement/) |

_13 labs, table generated by `scripts/gen_catalog.py`._
<!-- LABS:END -->

## Contributing

Contributions are welcome: read [CONTRIBUTING.md](./CONTRIBUTING.md), which
describes the anatomy of a lab of this repository and the golden rule, a lab is
tested both ways. The [code of conduct](./CODE_OF_CONDUCT.md) applies to every
exchange, and vulnerabilities are reported privately: [SECURITY.md](./SECURITY.md).

## License

This content is published under [Creative Commons Attribution 4.0
International](./LICENSE) (CC BY 4.0). You may share and adapt it, including
commercially, provided you credit the source.
