# Estimate a monthly cloud cost

Turn the supplied architecture into a transparent monthly estimate. The
fixture includes a dated exercise price grid; its prices are synthetic and are
not a quote from any cloud provider.

| | |
|---|---|
| Target | your machine, `challenge/work/` directory, no cloud account |
| Duration | about 30 minutes |
| Companion lesson | [the lesson on the site, in French](https://www.stephane-robert.info/docs/cloud/fondamentaux/pay-as-you-go-modeles-tarifaires/) |

```bash
dsoxlab run   estimer-cout-mensuel
dsoxlab check estimer-cout-mensuel
```

The challenge asks you to account for compute hours, block and object storage,
snapshots, requests and outbound data transfer. State your assumptions and
compare the total with the monthly budget.
