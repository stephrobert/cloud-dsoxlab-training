# Security policy

**Language:** [English](./SECURITY.md) · [Français](./SECURITY.fr.md)

## Supported versions

`cloud-dsoxlab-training` is under active development. Security fixes
are applied to the latest version of the `main` branch.

| Version | Supported |
| --- | --- |
| latest (`main`) | yes |
| older | no |

## Reporting a vulnerability

**Do not open a public issue for a security vulnerability.**

If you believe you have found one, report it privately:

- Preferred: open a
  [private security advisory](https://github.com/stephrobert/cloud-dsoxlab-training/security/advisories/new)
  on GitHub.
- Otherwise, use the contact details published on
  <https://www.stephane-robert.info>.

Please include:

- a description of the vulnerability and its impact,
- the steps to reproduce it (command, environment, `feint version`, `scw version`,
  `dsoxlab --version`),
- any relevant logs or proof of concept.

We will keep you posted on the fix and credit you in the release notes if you
wish.

## Disclosure policy

We practise coordinated disclosure and commit to the following timelines,
counted from the moment we receive your report:

| Step | Target |
| --- | --- |
| Acknowledging your report | within **48 hours** |
| Initial assessment and severity triage | within **5 days** |
| Fix released, or a written remediation plan | within **30 days** |
| Public disclosure of the vulnerability | within **90 days** |

We publish the advisory as soon as a fix is available, or at the **90-day** mark
at the latest, whichever comes first. If a vulnerability is being actively
exploited, we may disclose sooner to protect users. If a complex fix needs more
time, we tell you before the deadline and agree a new date with you, rather than
letting it lapse in silence.

## Scope

This repository ships **lab content**: briefs, fixtures, `setup.yaml` and
`cleanup.yaml` playbooks played on the learner's machine, pytest tests that read
the feint emulator and Incus machines, and encrypted reference solutions, all
run by the external `dsoxlab` CLI.

The labs start two things on the host, and that is where vigilance goes: the
**feint container**, at an image pinned by digest, published on `127.0.0.1`
only; and, for the "A first clean VM" lab, an **Incus virtual machine** on a
dedicated private network, destroyed by `dsoxlab clean`.

The fixtures carry **dummy credentials**, those `feint env` produces to point
`scw` and `octl` at the emulator: well-formed, they open nothing at any
provider. CodeQL analyses neither `labs/**/fixtures/**` nor `solution/**` (see
[`.github/codeql/config.yml`](.github/codeql/config.yml)). What the repository
ships as **its own** tooling (workflows, validation scripts, playbooks, pytest
tests) stays fully analysed.

In scope:

- dangerous or malicious lab material, notably a playbook or a test that would
  reach an undeclared destination, publish feint beyond `127.0.0.1` or
  exfiltrate data from the learner's machine;
- a leak of a real secret, a private key or an API token committed by mistake;
- a reference solution shipped in clear text, which spoils the lab and stays in
  the history;
- an action or an image referenced without pinning by SHA or digest in what the
  repository ships as reference.

Out of scope:

- vulnerabilities of the `dsoxlab` engine itself, which belong to
  [its own repository](https://github.com/stephrobert/dsoxlab);
- those of feint, `scw`, `octl`, Incus or any third-party dependency, to be
  reported to their respective projects;
- a lab that fails or grades wrongly: that is a defect, open a public issue.

## What this repository will never ask you

No lab requires a cloud account, a credit card or a real secret. If a brief
asks you for credentials of a real provider, that is a defect of the catalog:
report it.
