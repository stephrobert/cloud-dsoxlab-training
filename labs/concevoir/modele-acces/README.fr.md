# Concevoir un modèle d'identité et d'accès cloud

Concevez le système d'accès avant de le rattacher à l'implémentation IAM d'un
fournisseur.

| | |
|---|---|
| Cible | votre poste, répertoire `challenge/work/`, sans compte cloud |
| Durée | environ 40 minutes |
| Page associée | [la leçon du site](https://www.stephane-robert.info/docs/cloud/securite/iam/) |

```bash
dsoxlab run   concevoir-modele-acces
dsoxlab check concevoir-modele-acces
```

## Ce que vous saurez faire

- Définir la fédération des identités, les sessions courtes et les accès de
  secours strictement contrôlés.
- Séparer les responsabilités sensibles et désigner les responsables du cycle
  de vie des habilitations.
- Préciser les événements d'audit, leur conservation, leurs lecteurs et les
  alertes.

## Limite de la preuve

Cet exercice conçoit un modèle indépendant du fournisseur. Il ne crée pas
d'identités et ne prouve pas l'application des droits par un IAM réel.

Voir les leçons :
<https://www.stephane-robert.info/docs/cloud/securite/iam/>
et
<https://www.stephane-robert.info/docs/cloud/securite/moindre-privilege/>.
