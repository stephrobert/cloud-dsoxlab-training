#!/usr/bin/env bash
# Rejoue les tests de TOUS les labs contre leur solution de référence, et dans
# les deux sens.
#
# Dans les catalogues Terraform et DevSecOps, une fixture autouse du conftest
# pose la solution avant les tests, et `pytest labs/` suffit. Ici, non : un lab
# de ce catalogue démarre feint ou une machine Incus, et cela ne se rejoue pas
# depuis une fixture pytest. Ce script délègue donc à
# `scripts/verify-solutions.py`, qui démarre les services, joue `setup.yaml`,
# pose la solution, lance les tests, puis nettoie, sans dsoxlab.
#
# Pour UN lab, dans le parcours réel de l'apprenant, préférer :
#     python3 scripts/valider-labs.py --lab <id>
#
# Prérequis :
#   - feint, scw, octl, uv et Python aux versions de mise.toml (`mise install`) ;
#   - Docker et Incus qui répondent ;
#   - .vault-pass présent (les solutions sont chiffrées), sinon le script se
#     replie sur solution-en-clair/, jamais versionné.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_DIR}"

log()  { echo -e "\033[0;34m[test-all]\033[0m $*"; }
ok()   { echo -e "\033[0;32m[OK]\033[0m $*"; }
fail() { echo -e "\033[0;31m[FAIL]\033[0m $*" >&2; }

if [[ ! -d labs ]]; then
    fail "labs/ introuvable : à lancer depuis la racine du dépôt."
    exit 1
fi

# Un catalogue vide doit ÉCHOUER, pas passer en silence.
lab_count="$(find labs -name lab.yaml | wc -l)"
if [[ "${lab_count}" -eq 0 ]]; then
    fail "aucun lab trouvé sous labs/ : catalogue vide ?"
    exit 1
fi
log "${lab_count} labs, rejoués dans les deux sens sans dsoxlab"

if python3 scripts/verify-solutions.py --deux-sens --check "$@"; then
    ok "tous les labs passent"
else
    fail "au moins un lab échoue (voir ci-dessus)"
    exit 1
fi
