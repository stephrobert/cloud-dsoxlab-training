# Concevoir un tier applicatif élastique

Transformez les mesures fournies en plan d'élasticité. Externalisez les
sessions et les fichiers téléversés, rendez les requêtes sûres à réessayer et
précisez les contrôles de santé et de disponibilité avant de faire varier le
nombre de réplicas.

| | |
|---|---|
| Cible | votre poste, répertoire `challenge/work/`, sans compte cloud |
| Durée | environ 35 minutes |
| Page associée | [la leçon du site](https://www.stephane-robert.info/docs/cloud/fondamentaux/elasticite-vs-scalabilite/) |

```bash
dsoxlab run   concevoir-elasticite
dsoxlab check concevoir-elasticite
```

Calculez le nombre minimal de réplicas qui sert le pic soutenu même après la
perte d'une instance. Décrivez le scale-out et le scale-in avec des seuils
distincts, des fenêtres d'observation, un cooldown et le drainage des
connexions. L'exercice évalue un livrable de conception ; il ne déploie pas
d'autoscaler et ne prétend pas tester une panne réelle.
