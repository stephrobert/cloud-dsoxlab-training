# Politique de sécurité

**Langue :** [English](./SECURITY.md) · [Français](./SECURITY.fr.md)

## Versions supportées

`cloud-dsoxlab-training` est en développement actif. Les correctifs de
sécurité sont appliqués à la dernière version de la branche `main`.

| Version | Supportée |
| --- | --- |
| dernière (`main`) | oui |
| plus anciennes | non |

## Signaler une vulnérabilité

**N'ouvrez pas d'issue publique pour une vulnérabilité de sécurité.**

Si vous pensez avoir trouvé une vulnérabilité, signalez-la en privé :

- De préférence : ouvrez un
  [avis de sécurité privé](https://github.com/stephrobert/cloud-dsoxlab-training/security/advisories/new)
  sur GitHub.
- Sinon, utilisez les coordonnées publiées sur
  <https://www.stephane-robert.info>.

Merci d'inclure :

- une description de la vulnérabilité et de son impact,
- les étapes pour la reproduire (commande, environnement, `feint version`, `scw version`,
  `dsoxlab --version`),
- tout journal ou preuve de concept pertinent.

Nous vous tiendrons informé de l'avancement du correctif et vous créditerons
dans les notes de version si vous le souhaitez.

## Politique de divulgation

Nous pratiquons la divulgation coordonnée et nous engageons sur les délais
suivants, décomptés à partir de la réception de votre signalement :

| Étape | Délai visé |
| --- | --- |
| Accusé de réception de votre signalement | sous **48 heures** |
| Évaluation initiale et qualification de la sévérité | sous **5 jours** |
| Correctif publié, ou plan de remédiation écrit | sous **30 jours** |
| Divulgation publique de la vulnérabilité | sous **90 jours** |

Nous publions l'avis de sécurité dès qu'un correctif est disponible, ou au plus
tard à l'échéance des **90 jours**, selon ce qui arrive en premier. Si une
vulnérabilité est activement exploitée, nous pouvons la divulguer plus tôt pour
protéger les utilisateurs. Si un correctif complexe demande plus de temps, nous
vous prévenons avant l'échéance et convenons d'une nouvelle date avec vous,
plutôt que de la laisser expirer sans rien dire.

## Périmètre

Ce dépôt livre du **contenu de labs** : des énoncés, des fixtures, des
playbooks `setup.yaml` et `cleanup.yaml` joués sur la machine de l'apprenant,
des tests pytest qui lisent l'émulateur feint et des machines Incus, et des
solutions de référence chiffrées, le tout exécuté par la CLI externe `dsoxlab`.

Les labs lancent deux choses sur le poste, et c'est là que la vigilance porte :
le **conteneur feint**, à une image épinglée par digest, publié sur
`127.0.0.1` seulement ; et, pour le lab « Première VM propre », une **machine
virtuelle Incus** sur un réseau privé dédié, détruite par `dsoxlab clean`.

Les fixtures portent des **identifiants fictifs**, ceux que `feint env`
produit pour pointer `scw` et `octl` sur l'émulateur : bien formés, ils
n'ouvrent rien chez aucun fournisseur. CodeQL n'analyse ni
`labs/**/fixtures/**` ni `solution/**` (voir
[`.github/codeql/config.yml`](.github/codeql/config.yml)). Ce que le dépôt livre
comme **son** outillage (workflows, scripts de validation, playbooks, tests
pytest) reste entièrement analysé.

Sont dans le périmètre :

- du matériel de lab dangereux ou malveillant, notamment un playbook ou un test
  qui contacterait une destination non déclarée, publierait feint hors de
  `127.0.0.1` ou exfiltrerait des données du poste de l'apprenant ;
- une fuite de secret réel, une clé privée ou un jeton d'API commité par
  erreur ;
- une solution de référence livrée en clair, qui gâche le lab et reste dans
  l'historique ;
- une action ou une image référencée sans épinglage par SHA ou par digest dans
  ce que le dépôt livre comme référence.

Ne sont pas dans le périmètre :

- les vulnérabilités du moteur `dsoxlab` lui-même, qui relèvent de
  [son propre dépôt](https://github.com/stephrobert/dsoxlab) ;
- celles de feint, de `scw`, d'`octl`, d'Incus ou de toute dépendance tierce,
  à signaler à leurs projets respectifs ;
- un lab qui échoue ou qui note mal : c'est un défaut, il s'ouvre en issue
  publique.

## Ce que ce dépôt ne vous demandera jamais

Aucun lab n'exige de compte cloud, de carte bancaire ni de secret réel. Si un
énoncé vous demande des identifiants d'un vrai fournisseur, c'est un défaut du
catalogue : signalez-le.
