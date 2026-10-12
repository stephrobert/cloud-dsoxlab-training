# Contribuer à cloud-dsoxlab-training

**Language:** [English](./CONTRIBUTING.md) · [Français](./CONTRIBUTING.fr.md)

Ce dépôt est un **catalogue de labs** consommé par la CLI
[`dsoxlab`](https://github.com/stephrobert/dsoxlab). Les contributions sont de
nouveaux labs de la formation Cloud, des correctifs et des traductions. La CLI
vit dans son propre dépôt : n'ajoutez pas de code moteur ici.

## Mise en place

```bash
uv tool install dsoxlab        # la CLI (outil externe)
git clone https://github.com/stephrobert/cloud-dsoxlab-training.git
cd cloud-dsoxlab-training
mise install                   # feint, scw, octl, uv et Python aux versions de mise.toml
dsoxlab validate-structure     # vérifier le contrat
```

Docker doit répondre (`docker info`) : feint tourne en conteneur, démarré par
dsoxlab. Le lab « Première VM propre » demande en plus Incus, utilisable sans
sudo, sur un poste capable de virtualiser.

## La règle d'or : un lab s'éprouve dans les deux sens

Un test qui passe ne prouve rien tant qu'on n'a pas vu **échouer** ce qui doit
échouer. Avant de commiter un lab :

```bash
python3 scripts/valider-labs.py --lab <id>                     # par dsoxlab
python3 scripts/verify-solutions.py --deux-sens --lab <section>/<lab>   # sans dsoxlab
```

Le premier enchaîne les vraies commandes de l'apprenant (`run`, `check` qui
doit rendre 0, la solution, `check` qui doit rendre 100, `clean`) et consigne
le verdict dans `validation-labs.json`, avec les versions des outils. Il
signale aussi tout conteneur, toute instance ou tout réseau Incus laissé
derrière. Le second rejoue la même chose sans dsoxlab, en démarrant lui-même
feint et en jouant `setup.yaml` : retirer l'outil doit laisser les labs
jouables.

Éprouvez aussi chaque test contre une solution **fautive** : une instance
dotée d'une IP publique, une table de routage oubliée, un inventaire limité à
la zone par défaut. Le test visé doit tomber, et lui seul.

## Ce que les tests doivent lire

L'**état**, jamais ce que l'apprenant a tapé :

```python
# NON : on relit l'historique ou un script de l'apprenant
assert "ip=none" in historique

# OUI : on lit la ressource dans feint, par l'API du fournisseur
serveur = scw_get("/instance/v1/zones/fr-par-1/servers")["servers"][0]
assert serveur["public_ip"] is None
```

`conftest.py` expose les portes : `scw_get()` et `osc_call()` pour feint,
`hote_incus()` pour entrer dans une machine Incus par testinfra,
`incus_instance()` pour sa description. Un lab sur feint ne prouve jamais le
trafic : l'énoncé le dit, et aucun test ne prétend le contraire.

## Anatomie d'un lab

```text
labs/<section>/<lab>/
├── lab.yaml            # le contrat (id, level, runtime, fixtures, services, validation…)
├── lab.fr.yaml         # surcharge FR du title/description UNIQUEMENT
├── README.md / README.fr.md        # la leçon : prérequis, étapes, limite
├── scenario.md / scenario.fr.md    # la situation et la compétence visée
├── setup.yaml / cleanup.yaml       # optionnels : joués sur le poste (localhost)
├── fixtures/           # ce que `run` copie dans challenge/work
└── challenge/
    ├── README.md / README.fr.md    # la mission, tâches notées
    ├── hints.yaml                  # indices en base64, coûts 10, 15 et 20
    └── tests/test_functional.py    # la preuve
solution/<section>/<lab>/           # solution de référence, chiffrée par ansible-vault
```

Un lab sur feint déclare le service dans `runtime.services`, à l'image
**épinglée par digest**, et son `setup.yaml` remet l'émulateur à zéro
(`PUT /_feint/state` avec un état vide) : dsoxlab réutilise le conteneur d'un
lab à l'autre. Un lab qui pose un état tiré au hasard range sa référence dans
`lab_state_dir`, hors du répertoire de travail.

## Proposer un lab

- **Partir du contrat de la formation** : le module, le niveau (A ou B) et la
  limite du dispositif sont fixés là, pas dans le lab.
- **Citer la compétence éprouvée**, dans les deux scénarios : « Compétence
  visée : `cloud.x.y` » et « Skill targeted: `cloud.x.y` », et la porter dans
  les `skills` du `lab.yaml`. `tests/test_curriculums.py` le vérifie.
- **Faire pointer `doc_url` vers la leçon française** qui porte le lab : la CLI
  le lit, et le site reprend le titre du `lab.fr.yaml` mot pour mot.
- **Jouer chaque commande de l'énoncé** avant de l'écrire, contre feint ou sur
  la machine : un énoncé qui n'a pas été joué n'est pas livré.

## Vérifications locales avant d'ouvrir une PR

```bash
dsoxlab validate-structure                                   # le contrat meta.yml + lab.yaml
python3 scripts/valider-labs.py                              # chaque lab dans les deux sens, par dsoxlab
python3 scripts/verify-solutions.py --deux-sens              # la même chose, sans dsoxlab
uv run --no-project --with pytest --with pyyaml --with jsonschema pytest tests -q   # méta-tests
python3 scripts/gen_doc_url_en.py <chemin du dépôt du site>  # la table des traductions
python3 scripts/gen_catalog.py                               # rafraîchir le catalogue du README
```

## Conventions

- **Id de lab :** `<section>-<slug>`, où `<section>/<slug>` est son chemin sous
  `labs/` : `reseau-prive-scaleway` vit dans `labs/reseau/prive-scaleway`.
- **Commits :** en français, sujet factuel qui dit **ce qui a changé et
  pourquoi**, sans préfixe conventionnel. Le corps raconte ce qui a été mesuré.
- **i18n :** le fichier sans suffixe est l'anglais (langue officielle du dépôt),
  le `*.fr.md` est la traduction française. Les deux disent la même chose.
- **Style :** pas d'emoji ni de tiret cadratin dans ce que l'apprenant lit. Les
  messages d'assertion enseignent : ils disent ce qui ne va pas et pourquoi.

## Pull requests

Travaillez sur une branche dédiée, gardez `dsoxlab validate-structure` vert,
écrivez une description claire et reliez le lab ou l'issue traitée.
