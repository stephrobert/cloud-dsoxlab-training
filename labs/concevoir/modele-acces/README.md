# Design a cloud identity and access model

Design the access system before binding it to a provider's IAM implementation.

| | |
|---|---|
| Target | your machine, `challenge/work/` directory, no cloud account |
| Duration | about 40 minutes |
| Companion lesson | [the lesson on the site, in French](https://www.stephane-robert.info/docs/cloud/securite/iam/) |

```bash
dsoxlab run   concevoir-modele-acces
dsoxlab check concevoir-modele-acces
```

## What you will be able to do

- Specify workforce federation, short sessions and tightly controlled
  emergency access.
- Separate sensitive duties and assign owners for the access lifecycle.
- Define audit events, retention, readers and alerts.

## Evidence boundary

This is a provider-neutral design exercise. It does not create identities or
prove a provider's IAM enforcement.

See the lessons:
<https://www.stephane-robert.info/docs/cloud/securite/iam/>
and
<https://www.stephane-robert.info/docs/cloud/securite/moindre-privilege/>.
