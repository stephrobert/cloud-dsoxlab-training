# Estimer un coût cloud mensuel

Transformez le dossier d'architecture fourni en une estimation mensuelle
explicite. La fixture contient une grille d'exercice datée ; les prix sont
synthétiques et ne constituent pas un devis d'un fournisseur cloud.

| | |
|---|---|
| Cible | votre poste, répertoire `challenge/work/`, sans compte cloud |
| Durée | environ 30 minutes |
| Page associée | [la leçon du site](https://www.stephane-robert.info/docs/cloud/fondamentaux/pay-as-you-go-modeles-tarifaires/) |

```bash
dsoxlab run   estimer-cout-mensuel
dsoxlab check estimer-cout-mensuel
```

Le challenge vous demande de compter les heures de calcul, le stockage bloc et
objet, les snapshots, les requêtes et le trafic sortant. Indiquez vos
hypothèses et comparez le total au budget mensuel.
