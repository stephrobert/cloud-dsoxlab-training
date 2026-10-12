# Contributing to cloud-dsoxlab-training

**Language:** [English](./CONTRIBUTING.md) · [Français](./CONTRIBUTING.fr.md)

This repository is a **lab catalog** consumed by the
[`dsoxlab`](https://github.com/stephrobert/dsoxlab) CLI. Contributions are new
labs of the Cloud course, fixes and translations. The CLI lives in its own
repository: do not add engine code here.

## Setup

```bash
uv tool install dsoxlab        # the CLI (external tool)
git clone https://github.com/stephrobert/cloud-dsoxlab-training.git
cd cloud-dsoxlab-training
mise install                   # feint, scw, octl, uv and Python at the versions in mise.toml
dsoxlab validate-structure     # check the contract
```

Docker must answer (`docker info`): feint runs in a container, started by
dsoxlab. The "A first clean VM" lab also needs Incus, usable without sudo, on a
host able to virtualise.

## The golden rule: a lab is tested both ways

A passing test proves nothing until you have seen **fail** what must fail.
Before committing a lab:

```bash
python3 scripts/valider-labs.py --lab <id>                     # through dsoxlab
python3 scripts/verify-solutions.py --deux-sens --lab <section>/<lab>   # without dsoxlab
```

The first chains the learner's real commands (`run`, `check` that must return
0, the solution, `check` that must return 100, `clean`) and records the verdict
in `validation-labs.json`, with the tool versions. It also reports any
container, Incus instance or Incus network left behind. The second replays the
same without dsoxlab, starting feint itself and playing `setup.yaml`: removing
the tool must leave the labs playable.

Also test each test against a **faulty** solution: an instance with a public
IP, a forgotten route table, an inventory limited to the default zone. The
targeted test must fall, and it alone.

## What the tests must read

The **state**, never what the learner typed:

```python
# NO: reading the learner's history or script
assert "ip=none" in history

# YES: reading the resource in feint, through the provider's API
server = scw_get("/instance/v1/zones/fr-par-1/servers")["servers"][0]
assert server["public_ip"] is None
```

`conftest.py` exposes the doors: `scw_get()` and `osc_call()` for feint,
`hote_incus()` to enter an Incus machine through testinfra, `incus_instance()`
for its description. A lab on feint never proves traffic: the brief says so,
and no test claims otherwise.

## Anatomy of a lab

```text
labs/<section>/<lab>/
├── lab.yaml            # the contract (id, level, runtime, fixtures, services, validation…)
├── lab.fr.yaml         # FR override of title/description ONLY
├── README.md / README.fr.md        # the lesson: prerequisites, steps, limit
├── scenario.md / scenario.fr.md    # the situation and the skill targeted
├── setup.yaml / cleanup.yaml       # optional: played on the host (localhost)
├── fixtures/           # what `run` copies into challenge/work
└── challenge/
    ├── README.md / README.fr.md    # the mission, graded tasks
    ├── hints.yaml                  # hints in base64, costs 10, 15 and 20
    └── tests/test_functional.py    # the proof
solution/<section>/<lab>/           # reference solution, encrypted with ansible-vault
```

A lab on feint declares the service in `runtime.services`, with the image
**pinned by digest**, and its `setup.yaml` resets the emulator
(`PUT /_feint/state` with an empty state): dsoxlab reuses the container from one
lab to the next. A lab that lays down a randomly drawn state stores its
reference in `lab_state_dir`, outside the working directory.

## Proposing a lab

- **Start from the course contract**: the module, the level (A or B) and the
  limit of the device are set there, not in the lab.
- **Name the skill tested**, in both scenarios: "Compétence visée :
  `cloud.x.y`" and "Skill targeted: `cloud.x.y`", and carry it in the `skills`
  of `lab.yaml`. `tests/test_curriculums.py` checks it.
- **Point `doc_url` at the French lesson** that carries the lab: the CLI reads
  it, and the site reuses the `lab.fr.yaml` title word for word.
- **Play every command of the brief** before writing it, against feint or on the
  machine: a brief that was not played is not delivered.

## Local checks before opening a PR

```bash
dsoxlab validate-structure                                   # the meta.yml + lab.yaml contract
python3 scripts/valider-labs.py                              # every lab both ways, through dsoxlab
python3 scripts/verify-solutions.py --deux-sens              # the same, without dsoxlab
uv run --no-project --with pytest --with pyyaml --with jsonschema pytest tests -q   # meta-tests
python3 scripts/gen_doc_url_en.py <path to the site repository>  # the translation table
python3 scripts/gen_catalog.py                               # refresh the README catalog
```

## Conventions

- **Lab id:** `<section>-<slug>`, where `<section>/<slug>` is its path under
  `labs/`: `reseau-prive-scaleway` lives in `labs/reseau/prive-scaleway`.
- **Commits:** in French, a factual subject that says **what changed and
  why**, with no conventional prefix. The body tells what was measured.
- **i18n:** the file without a suffix is English (the repository's official
  language), the `*.fr.md` is the French translation. Both say the same thing.
- **Style:** no emoji and no em dash in what the learner reads. Assertion
  messages teach: they say what is wrong and why.

## Pull requests

Work on a dedicated branch, keep `dsoxlab validate-structure` green, write a
clear description and link the lab or the issue addressed.
