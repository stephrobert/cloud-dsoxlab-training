"""Méta-tests du dépôt : une compétence citée existe, et le lab la porte.

Chaque lab éprouve une compétence `cloud.*` de la formation, et son scénario
le dit dans les deux langues :

    Compétence visée : `cloud.network.design`
    Skill targeted: `cloud.network.design`

Un identifiant de compétence se trompe sans bruit : `cloud.cost.estimate` et
`cloud.finops.optimize` parlent tous deux de coût. Repris du test du catalogue
DevSecOps, qui ferme le même défaut sur les pratiques du NIST SSDF, adapté à la
grille de ce catalogue (`curriculums.yml`).

Trois contrôles :

- la grille porte sa source et sa date ;
- chaque scénario cite au moins une compétence, et elle existe ;
- la compétence citée figure aussi dans les `skills` du `lab.yaml`, que le
  site lit pour rattacher le lab à sa compétence : deux descriptions du même
  lab qui divergent, c'est la seconde que le site croit.
"""

import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
LABS = REPO / "labs"
SOURCE = REPO / "curriculums.yml"

FICHIERS_LUS = ("scenario.fr.md", "scenario.md")
CITATION = re.compile(
    r"(?:Compétences? visées?|Skills? targeted)\s*:\s*(?P<suite>[^\n]+)"
)
IDENTIFIANT = re.compile(r"`(?P<id>cloud\.[a-z]+\.[a-z]+)`")


def grille() -> dict:
    return yaml.safe_load(SOURCE.read_text(encoding="utf-8"))["curriculums"]["cloud"]


def tous_les_labs() -> list[str]:
    return sorted(str(c.parent.relative_to(LABS)) for c in LABS.rglob("lab.yaml"))


def citations(rel: str, nom: str) -> list[str]:
    chemin = LABS / rel / nom
    if not chemin.is_file():
        return []
    trouvees = []
    for ligne in CITATION.finditer(chemin.read_text(encoding="utf-8")):
        trouvees += [m.group("id") for m in IDENTIFIANT.finditer(ligne.group("suite"))]
    return trouvees


def test_la_grille_porte_sa_provenance() -> None:
    g = grille()
    assert g["source"].startswith("https://"), "La grille ne cite pas sa source."
    assert g["derniere_verification"], "La grille ne dit pas quand elle a été confrontée."


def test_la_grille_porte_les_dix_huit_candidates() -> None:
    """Le contrat en arrête 18 (§3.2), chacune titrée dans les deux langues."""
    competences = grille()["competences"]
    assert len(competences) == 18, f"La grille porte {len(competences)} compétences, 18 attendues."
    sans_titre = [c for c, t in competences.items() if not (t.get("fr") and t.get("en"))]
    assert not sans_titre, f"Compétences sans titre FR et EN : {sans_titre}."


@pytest.mark.parametrize("rel", tous_les_labs())
@pytest.mark.parametrize("nom", FICHIERS_LUS)
def test_chaque_scenario_cite_une_competence_connue(rel: str, nom: str) -> None:
    citees = citations(rel, nom)
    assert citees, (
        f"{rel}/{nom} ne cite aucune compétence. Ajoutez la ligne "
        "« Compétence visée : `cloud.x.y` » ou « Skill targeted: `cloud.x.y` »."
    )
    inconnues = sorted(set(citees) - set(grille()["competences"]))
    assert not inconnues, f"{rel}/{nom} cite {inconnues}, absente(s) de curriculums.yml."


@pytest.mark.parametrize("rel", tous_les_labs())
def test_le_lab_porte_la_competence_qu_il_annonce(rel: str) -> None:
    skills = set(yaml.safe_load((LABS / rel / "lab.yaml").read_text(encoding="utf-8"))["skills"])
    citees = set(citations(rel, "scenario.fr.md")) | set(citations(rel, "scenario.md"))
    absentes = sorted(citees - skills)
    assert not absentes, (
        f"{rel} annonce {absentes} dans son scénario, mais son lab.yaml ne les "
        "porte pas dans `skills`."
    )
