# Challenge : défendre la revue d'architecture

Lisez `review-evidence.json` et écrivez deux fichiers dans le répertoire de
travail (`challenge/work/`) :

- `review.json`, avec les six notes, les preuves citées, les trois risques les
  plus graves, les décisions ADR, les responsables, les échéances et les limites
  des preuves ;
- `review.md`, un rapport concis pour le comité d'architecture.

Notez chacun des six axes (`operational-excellence`, `security`, `reliability`,
`performance`, `cost`, `sovereignty`) de 0 à 3 avec cette grille, d'après le
type et le contenu de ses preuves :

| Note | Les preuves de l'axe |
|---|---|
| 3 | un test ou une mesure vérifiés et datés montrent l'exigence tenue |
| 2 | une configuration ou une estimation montrent l'exigence tenue, sans vérification |
| 1 | montrent l'exigence non tenue, ou non évaluée |
| 0 | il n'y en a pas |

Les `risks` du pack de preuves se classent par gravité multipliée par
probabilité. Retenez les trois plus graves et, pour chacun, consignez une
décision (`correct`, `accept` ou `defer`), une raison, un responsable, une
échéance et une action. Un risque accepté nomme la personne qui l'accepte.

Déclarez toutes les `evidence_limits` fournies : cet exercice ne prouve ni une
facture réelle d'un fournisseur, ni l'application de l'IAM, ni le comportement
du dataplane.

Lancez `dsoxlab check defendre-revue-architecture` pour voir le résultat.
