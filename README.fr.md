# Formation Cloud : pratiquer sans compte

**Langue :** [English](./README.md) · [Français](./README.fr.md)

[![CI](https://github.com/stephrobert/cloud-dsoxlab-training/actions/workflows/ci.yml/badge.svg)](https://github.com/stephrobert/cloud-dsoxlab-training/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/stephrobert/cloud-dsoxlab-training?label=OpenSSF%20Scorecard)](https://securityscorecards.dev/viewer/?uri=github.com/stephrobert/cloud-dsoxlab-training)
[![Plumber compliance](https://score.getplumber.io/github.com/stephrobert/cloud-dsoxlab-training.svg)](https://score.getplumber.io/github.com/stephrobert/cloud-dsoxlab-training)
[![SLSA 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)
[![Licence : CC BY 4.0](https://img.shields.io/badge/Licence-CC%20BY%204.0-lightgrey.svg)](./LICENSE)

Labs de la [formation Cloud](https://blog.stephane-robert.info/docs/cloud/) de
blog.stephane-robert.info, pilotés par la CLI
[`dsoxlab`](https://github.com/stephrobert/dsoxlab) et joués **sans compte
cloud ni carte bancaire**. Les CLI officielles des fournisseurs, `scw` pour
Scaleway et `octl` pour Outscale, y pilotent **feint**, un émulateur local de
leurs API ; **Incus** démarre les machines qui doivent réellement démarrer.

## Ce que c'est

`cloud-dsoxlab-training` est un **dépôt de contenu**, pas une application. Il
fournit :

- des **labs guidés** (niveau A du contrat de la formation), qui font
  pratiquer un geste avec les commandes données ;
- des **challenges**, sans procédure ni indice gratuit, qui produisent la
  preuve d'une compétence ;
- une **validation automatique** qui lit l'**état** laissé par l'apprenant,
  dans l'émulateur par les API publiques des fournisseurs, ou dans la machine
  par testinfra, jamais les commandes tapées ;
- une **grille d'objectifs**, les compétences `cloud.*` de la formation : chaque
  lab cite celle qu'il éprouve ;
- un **score** avec des indices à coût croissant.

## Ce que feint prouve, et ce qu'il ne prouve pas

feint sert le **contrat d'API** de Scaleway et d'Outscale : les ressources
existent, avec leurs liens, et se lisent comme chez le fournisseur. Il
n'achemine **aucun paquet**, n'applique ni routage ni NAT, n'émule ni prix, ni
quotas, ni IAM. Un lab réseau sur feint prouve donc qu'une architecture est
**déclarée** correctement, pas que le trafic sort. La leçon
[Ce que feint prouve](https://blog.stephane-robert.info/docs/cloud/outils/feint/limites/)
le détaille, et chaque lab concerné le rappelle dans son énoncé.

## Prérequis

- Python 3.11+ et [`uv`](https://docs.astral.sh/uv/), `git`.
- **Docker qui répond** (`docker info`) : feint tourne en conteneur, image
  épinglée par digest, démarré et arrêté par dsoxlab. Le port **4599** doit
  être libre.
- **[`mise`](https://mise.jdx.dev/)**, qui pose feint, `scw` et `octl` aux
  versions de `mise.toml` (`mise install`).
- Pour le lab « Première VM propre » seulement : **Incus** utilisable sans sudo,
  sur un poste capable de virtualiser
  ([installer Incus](https://blog.stephane-robert.info/docs/conteneurs/moteurs-conteneurs/incus/installation/)).

## Installation

```bash
# 1. Installer la CLI dsoxlab (outil externe, hors de ce dépôt)
uv tool install dsoxlab        # ou : pipx install dsoxlab

# 2. Cloner ce catalogue de labs, et poser ses outils
git clone https://github.com/stephrobert/cloud-dsoxlab-training.git
cd cloud-dsoxlab-training
mise install

# 3. Vérifier que le contrat est valide
dsoxlab validate-structure
```

### Votre premier lab, en cinq minutes

```bash
dsoxlab list-labs                            # parcourir le catalogue
dsoxlab run       reseau-prive-scaleway      # démarrer feint, poser l'état de départ
dsoxlab challenge reseau-prive-scaleway      # lire la mission
cd labs/reseau/prive-scaleway/challenge/work
source feint-scaleway.env                    # pointer scw sur l'émulateur
# ... vous construisez le réseau avec scw ...
dsoxlab check     reseau-prive-scaleway      # valider et noter
dsoxlab clean     reseau-prive-scaleway      # arrêter feint, tout retirer
```

Un seul lab sur feint à la fois : les labs partagent le même service, que
`run` remet à zéro. Bloqué ? `dsoxlab hint <id>` révèle un indice, dont le coût
est déduit du score.

### Garder à jour

```bash
git pull                       # le catalogue
uv tool upgrade dsoxlab        # le moteur
mise install                   # les outils épinglés
```

Un lab qui échoue après une montée de version de feint, de `scw` ou d'`octl`
est un défaut du catalogue : ouvrez une issue, le formulaire arrive prérempli
par `dsoxlab support --issue`.

## Comment ça marche

### Le contrat déclaratif, à deux niveaux

- **`meta.yml`**, à la racine, déclare l'identité du dépôt, l'**ordre** des
  labs, celui du parcours du blog, et réserve le réseau du catalogue
  (`lab-cloud`, `10.10.70.0/24`) pour les labs sur machine à venir ;
- **`lab.yaml`**, par lab, déclare ses `skills`, son `level`, son `runtime`
  (type, fixtures, **services**), son `doc_url` et un bloc `validation`. Un
  `lab.fr.yaml` surcharge le `title` et la `description` en français.

### Les runtimes

| Runtime | Ce que le lab demande |
|---|---|
| `shell` + service feint | un terminal, Docker et les CLI de `mise.toml`. dsoxlab démarre feint, le `setup.yaml` le remet à zéro (et, pour un challenge, y déclare l'environnement à lire). |
| `shell` + Incus | un terminal et Incus. Le `setup.yaml` prépare un réseau privé dédié ; l'apprenant y démarre lui-même la machine ; `clean` la détruit avec son réseau. |

### Le modèle de validation

La validation **prouve l'état, elle ne fait pas confiance à l'apprenant**. Les
tests lisent feint par les API publiques de Scaleway et d'Outscale, ou entrent
dans la machine par `incus exec` et testinfra. Un challenge tiré au hasard
range son inventaire de référence **hors** du répertoire de travail, pour
refuser un environnement modifié.

Un lab s'éprouve **dans les deux sens** : les tests doivent échouer avant le
travail, et passer après. `scripts/valider-labs.py` l'atteste par les vraies
commandes dsoxlab dans `validation-labs.json` ; `scripts/verify-solutions.py
--deux-sens` le refait **sans dsoxlab**, en démarrant lui-même feint et en
jouant `setup.yaml` : retirer l'outil doit laisser les labs jouables.

Les solutions de référence vivent sous `solution/`, **chiffrées par
ansible-vault** : une solution livrée en clair gâche le lab, et git la garde
pour toujours.

### La grille d'objectifs : les compétences de la formation

Chaque scénario cite la compétence qu'il éprouve : « Compétence visée :
`cloud.network.design` ». `curriculums.yml` porte les 18 compétences de la
formation, et `tests/test_curriculums.py` refuse un identifiant absent de la
grille, ou une compétence annoncée que le `lab.yaml` ne porte pas.

### Les liens vers les guides

Le `doc_url` d'un lab est la leçon française, parce que dsoxlab le lit. Les
liens des README sont **calculés** : `scripts/gen_doc_url_en.py` lit les
`translationOf` du site, et `scripts/gen_catalog.py` fait pointer le README
anglais vers la traduction quand elle existe.

## Catalogue

<!-- LABS:START -->
### Pratiquer sans compte

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pratiquer-challenge-budget-contraint` | Challenge 1 : architecture à budget contraint | a | shell | [guide](https://blog.stephane-robert.info/docs/cloud/outils/feint/limites/) |

### Amorcer une machine

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `amorcer-premiere-vm-propre` | Première VM propre : amorcée par cloud-init, sans adresse publique | a | shell | [guide](https://blog.stephane-robert.info/docs/cloud/cloud-init/) |

### Réseau cloud

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `reseau-prive-scaleway` | Réseau privé, et premières instances sans adresse publique : scw sur feint | a | shell | [guide](https://blog.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/) |
| `reseau-prive-outscale` | Réseau privé, et premières instances sans adresse publique : octl sur feint | a | shell | [guide](https://blog.stephane-robert.info/docs/cloud/architecture/03-tables-routage-et-gateways/) |

_4 labs, table générée par `scripts/gen_catalog.py`._
<!-- LABS:END -->

## Contribuer et licence

Les contributions sont bienvenues : lisez
[CONTRIBUTING.fr.md](./CONTRIBUTING.fr.md), qui décrit l'anatomie d'un lab de ce
dépôt et la règle d'or, un lab s'éprouve dans les deux sens. Le
[code de conduite](./CODE_OF_CONDUCT.fr.md) s'applique à tous les échanges, et
les vulnérabilités se signalent en privé : [SECURITY.fr.md](./SECURITY.fr.md).

### Licence

Ce contenu est publié sous [Creative Commons Attribution 4.0
International](./LICENSE) (CC BY 4.0). Vous pouvez le partager et l'adapter, y
compris commercialement, à condition de citer la source.
