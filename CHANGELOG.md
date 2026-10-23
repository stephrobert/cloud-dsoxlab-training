# Changelog

**Language:** [English](./CHANGELOG.md) · [Français](./CHANGELOG.fr.md)

All notable changes to this project are recorded in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/).

This repository is a **content catalog**, not a library. A version is published
by a tag, which produces a signed archive (see [RELEASING.md](./RELEASING.md));
the unit that matters remains the lab.

## [0.2.2] - 2026-10-23

### Added

- A verdict can no longer be committed together with what it measures. The
  `verdicts-et-commun-separes` hook refuses a commit carrying
  `validation-labs.json` alongside anything the cycle plays:
  `challenge/tests/`, `setup.yaml`, `cleanup.yaml`, `lab.yaml` of any lab, and
  the shared tooling. It is itself tested, in both directions, by a hook of its
  own.

  This closes a case **no measurement can catch afterwards**. The staleness of
  a verdict used to be judged by comparing DATES, and that comparison was wrong
  in both directions on 2026-10-22: a correction committed together with the
  verdicts it invalidated passed as healthy, and labs re-attested on a branch
  came back "to be re-attested" after their squash merge, their content
  unchanged. When a squashed pull request touches a test *after* its campaign,
  the single commit carries both and the squash has destroyed what told them
  apart. It cannot be observed, so it is prevented.

  The statement stays allowed next to a verdict: it is not played by the cycle,
  and forbidding it would demand a campaign for a typo.

### Fixed

- `pipelineMustNotLeakSecretsInConfig` is removed from `.plumber.yaml`, where
  it was declared twice. Plumber dropped that control and answers "was removed
  and is now ignored: secret detection is no longer part of Plumber; remove
  this block". Keeping it suggested that secret detection was covered here. It
  is not, and `detect-private-key` is what comes closest, as a hook.

## [0.2.1] - 2026-10-19

### Changed

- **Every `doc_url` now points at `www.stephane-robert.info`.** The site moved
  from `blog.` to `www.`, and the old host redirects with a 301 to the same
  path. Nothing was broken: `validate-structure --check-urls` follows
  redirections, and this catalogue was green before a single line changed. The
  migration is housekeeping, not repair: a `doc_url` should point at the page
  rather than depend on a redirection that will be removed one day.

  The paths are identical between the two hosts, so only the host changed. The
  359 `doc_url` the catalogues declare were looked up in the site's own
  repository, offline: all of them exist there, including twenty-three pages
  the old host answered with a 404.

## [0.2.0] - 2026-10-17

### Changed

- **The validator reads the contract, not the terminal panel.**
  `scripts/valider-labs.py` parsed the score out of what `dsoxlab check`
  *displays*. That panel is interface: it changed in dsoxlab 0.4.0 and the
  regex stopped finding anything. It now reads `check --json`, which carries a
  `schema`, and the reading lives in `scripts/verdict_check.py`, **identical in
  all twelve catalogs**.

- **Three verdicts, not two.** A run where every collected test skipped
  measured nothing: it is **SKIP**, neither green nor red, and it stays to be
  measured. Painting it red would accuse the lab of what is missing from the
  machine. `--check` therefore exits `10` in that case, against `1` for a RED,
  mirroring `dsoxlab doctor --strict` where 9 is repaired and 10 is remeasured.

- **The README takes the reference structure** shared by the twelve catalogs:
  fourteen sections, in both languages. Seven of them describe dsoxlab rather
  than the subject, and are therefore identical everywhere.

### Requires

- **dsoxlab 0.4.1 or later**, which introduced the `status` field of
  `check --json`. Without it the validator refuses to conclude rather than
  guessing.

### Also

- la borne de version du moteur est déclarée dans la CI et dans le hook de pre-push.

## [0.1.1] - 2026-10-14

### Fixed

- "Feint" is capitalised in the private-network lab titles, in both
  languages.
- Two labs re-attested with dsoxlab 0.3.5.

### Changed

- The release procedure re-attests labs modified since their verdict.

## [0.1.0] - 2026-10-12

### Added

- **The catalog**, on the structure of the DevSecOps catalog, itself aligned on
  Kubernetes, Linux and Terraform: `meta.yml` and `meta.fr.yml` contract,
  `lab-cloud` network reserved in `10.10.70.0/24`, repository meta-tests,
  bilingual READMEs whose catalog is generated, CI and release chain taken over
  as is (zizmor, actionlint, poutine, Plumber, CodeQL, Scorecard, signed archive
  and SLSA provenance).
- **The objectives grid** (`curriculums.yml`): the 18 candidate `cloud.*` skills
  of the course contract. Each lab names the one it tests, and
  `tests/test_curriculums.py` checks it against its `skills`.
- **Wave 1 of the labs**, modules 2b, 2c and 3 of the course:
  - `pratiquer-challenge-budget-contraint`, challenge 1: an environment drawn
    at random in feint, read with `scw` and costed on an exercise grid dated
    2026-10-12;
  - `amorcer-premiere-vm-propre`: an Incus VM booted by cloud-init on a private
    network, checked with testinfra, destroyed by `clean`;
  - `reseau-prive-scaleway` and `reseau-prive-outscale`: the multi-zone private
    network declared on feint with `scw`, then with `octl`.
- **Two validation proofs**: `scripts/valider-labs.py`, through the real dsoxlab
  commands, and `scripts/verify-solutions.py`, without dsoxlab, which starts
  feint and plays `setup.yaml` itself.

### Measured

- The four labs return 0 before the work and 100 after it, with dsoxlab 0.3.1,
  feint v0.13.0 (image pinned by digest), scw 2.62.0, octl v0.0.32 and Incus
  7.2, with no container, instance or network left behind.
- Negative checks: a public IP on an instance only fails task 2 of the Scaleway
  lab; a private table not linked in `eu-west-2b` only fails task 5 of the
  Outscale lab; an inventory limited to the default zone scores 40/100 in the
  challenge; a deleted resource scores 0/100.
[0.1.1]: https://github.com/stephrobert/cloud-dsoxlab-training/releases/tag/v0.1.1
