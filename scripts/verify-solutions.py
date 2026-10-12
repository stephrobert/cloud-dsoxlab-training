#!/usr/bin/env python3
"""Rejoue les solutions de référence SANS dsoxlab, et prouve qu'elles marchent.

Raison d'être : une montée de version de feint, de scw, d'octl ou d'Incus peut
casser une solution sans que personne ne s'en aperçoive, parce que les tests
d'un lab ne tournent que si un apprenant le joue. Ce script rejoue **toutes**
les solutions avec les outils actuellement installés et enregistre le résultat
dans ``solution/verified-with.json``.

Il fait aussi le **test de non-couplage** que décrit la documentation de
dsoxlab : retirer l'outil doit laisser les labs jouables à la main. Le script
n'appelle donc jamais dsoxlab. Pour chaque lab :

1. il démarre lui-même les services déclarés (``runtime.services``), feint
   ici, à l'image épinglée du ``lab.yaml``, et attend leur sonde ;
2. il crée un répertoire de travail temporaire et un répertoire d'état, y
   copie les ``fixtures/``, et joue ``setup.yaml`` par ``ansible-playbook`` ;
3. il y pose la solution (déchiffrée depuis ``solution/``, ou lue dans
   ``solution-en-clair/`` tant que ``.vault-pass`` manque) et joue son
   ``solution.sh`` ;
4. il joue ``challenge/tests/test_functional.py`` avec ``LAB_WORKDIR`` et
   ``LAB_STATE_DIR`` ;
5. il joue ``cleanup.yaml`` et arrête les services, quoi qu'il arrive.

Avec ``--deux-sens``, il rejoue chaque lab sans la solution et exige qu'aucun
test ne passe : un test vrai avant le travail ne mesure rien.

``scripts/valider-labs.py`` fait l'autre preuve, celle du parcours réel de
l'apprenant, par les commandes dsoxlab. Les deux ne se remplacent pas.

Usage :

    python3 scripts/verify-solutions.py
    python3 scripts/verify-solutions.py --lab reseau/reseau-prive-scaleway
    python3 scripts/verify-solutions.py --deux-sens --check
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SOLUTIONS = REPO / "solution"
SOLUTIONS_EN_CLAIR = REPO / "solution-en-clair"
LABS = REPO / "labs"
RECORD = SOLUTIONS / "verified-with.json"
VAULT_PASS = REPO / ".vault-pass"
SCRIPT_SOLUTION = "solution.sh"
PREFIXE_SERVICE = "verif-solution-"


def outil_version(binaire: str, *args: str) -> str | None:
    """Première version x.y.z lue dans la sortie d'un outil, ou None."""
    if not shutil.which(binaire):
        return None
    try:
        proc = subprocess.run(
            [binaire, *args], capture_output=True, text=True, timeout=30, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    match = re.search(r"v?(\d+\.\d+(?:\.\d+)?)", proc.stdout + proc.stderr)
    return match.group(1) if match else None


def source_des_solutions() -> tuple[Path, bool]:
    """(répertoire, chiffré ?) : solution/ si le vault est là, sinon le clair."""
    if VAULT_PASS.is_file() and SOLUTIONS.is_dir():
        return SOLUTIONS, True
    return SOLUTIONS_EN_CLAIR, False


def solutions_disponibles() -> list[str]:
    """Chemins relatifs des labs ayant une solution, triés."""
    racine, _ = source_des_solutions()
    if not racine.is_dir():
        return []
    trouves = set()
    for fichier in racine.rglob("*"):
        if not fichier.is_file() or fichier.name == RECORD.name:
            continue
        candidat = fichier.parent
        while candidat != racine:
            if (LABS / candidat.relative_to(racine) / "lab.yaml").is_file():
                trouves.add(str(candidat.relative_to(racine)))
                break
            candidat = candidat.parent
    return sorted(trouves)


def dechiffrer(fichier: Path) -> bytes:
    """Contenu en clair d'un fichier de solution chiffré par ansible-vault."""
    with open(os.devnull) as entree:
        proc = subprocess.run(
            ["ansible-vault", "view", "--vault-password-file", str(VAULT_PASS), str(fichier)],
            stdin=entree, capture_output=True, check=False,
        )
    if proc.returncode != 0:
        raise RuntimeError(
            f"Déchiffrement impossible pour {fichier.name} : "
            f"{proc.stderr.decode(errors='replace').strip()}"
        )
    return proc.stdout


def jouer_script_de_solution(work: Path) -> None:
    """Exécute ``solution.sh`` s'il a été posé, puis le retire du workdir.

    Même mécanisme que ``conftest.py`` : le script est le moyen d'atteindre
    l'état attendu, il n'en fait pas partie. Son échec est bruyant.
    """
    script = work / SCRIPT_SOLUTION
    if not script.is_file():
        return
    proc = subprocess.run(
        ["bash", SCRIPT_SOLUTION], cwd=work, capture_output=True, text=True, check=False
    )
    script.unlink()
    if proc.returncode != 0:
        raise RuntimeError(
            f"La solution de référence a échoué (code {proc.returncode}).\n"
            f"--- stdout ---\n{proc.stdout[-2000:]}\n"
            f"--- stderr ---\n{proc.stderr[-2000:]}"
        )


def contrat(lab_rel: str) -> dict:
    return yaml.safe_load((LABS / lab_rel / "lab.yaml").read_text(encoding="utf-8")) or {}


def demarrer_services(services: list[dict]) -> list[str]:
    """Lance chaque service déclaré, attend sa sonde, rend les noms lancés."""
    lances = []
    for service in services:
        nom = PREFIXE_SERVICE + service["name"]
        subprocess.run(["docker", "rm", "-f", nom], capture_output=True, check=False)
        commande = ["docker", "run", "-d", "--name", nom]
        for port in service.get("ports") or []:
            commande += ["-p", port]
        commande += list(service.get("run_args") or [])
        commande.append(service["image"])
        proc = subprocess.run(commande, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            raise RuntimeError(f"service {service['name']} : {proc.stderr.strip()}")
        lances.append(nom)
        sonde = service.get("ready_exec") or []
        if isinstance(sonde, str):
            sonde = ["sh", "-c", sonde]
        limite = time.monotonic() + int(service.get("ready_timeout") or 90)
        while sonde:
            if subprocess.run(
                ["docker", "exec", nom, *sonde], capture_output=True, check=False
            ).returncode == 0:
                break
            if time.monotonic() > limite:
                raise RuntimeError(f"service {service['name']} jamais prêt")
            time.sleep(1)
    return lances


def arreter_services(noms: list[str]) -> None:
    for nom in noms:
        subprocess.run(["docker", "rm", "-f", nom], capture_output=True, check=False)


def jouer_playbook(lab_rel: str, nom: str, work: Path, etat: Path) -> None:
    playbook = LABS / lab_rel / nom
    if not playbook.is_file():
        return
    with open(os.devnull) as entree:
        proc = subprocess.run(
            [
                "ansible-playbook", "-i", "localhost,", "-c", "local", str(playbook),
                "-e", f"lab_id={contrat(lab_rel).get('id')}",
                "-e", f"lab_workdir={work}",
                "-e", f"lab_state_dir={etat}",
            ],
            stdin=entree, capture_output=True, text=True, check=False,
        )
    if proc.returncode != 0:
        raise RuntimeError(f"{nom} a échoué : {proc.stdout[-1500:]}{proc.stderr[-500:]}")


def poser_solution(lab_rel: str, work: Path) -> None:
    racine, chiffre = source_des_solutions()
    for fichier in sorted((racine / lab_rel).rglob("*")):
        if fichier.is_file():
            dst = work / fichier.relative_to(racine / lab_rel)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(dechiffrer(fichier) if chiffre else fichier.read_bytes())
    jouer_script_de_solution(work)


def rejouer(lab_rel: str, garder: bool = False, avec_solution: bool = True) -> tuple[bool, str]:
    """Joue la suite du lab contre la solution, ou contre l'état de départ seul.

    Avec la solution, le succès est « tous les tests passent ». Sans elle, le
    succès est « aucun test ne passe » : le point de départ ne doit rien valoir.
    """
    suite = LABS / lab_rel / "challenge" / "tests" / "test_functional.py"
    if not suite.is_file():
        return False, "suite de tests introuvable"

    runtime = contrat(lab_rel).get("runtime") or {}
    tmp = Path(tempfile.mkdtemp(prefix="verif-solution-"))
    work, etat = tmp / "work", tmp / "etat"
    work.mkdir()
    etat.mkdir()
    services: list[str] = []
    try:
        services = demarrer_services(runtime.get("services") or [])
        fixtures = LABS / lab_rel / "fixtures"
        for declaree in runtime.get("fixtures") or []:
            dst = work / declaree
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fixtures / declaree, dst)
        jouer_playbook(lab_rel, "setup.yaml", work, etat)
        if avec_solution:
            poser_solution(lab_rel, work)
        env = dict(os.environ, LAB_WORKDIR=str(work), LAB_STATE_DIR=str(etat))
        # Le python du poste n'a ni pytest ni testinfra : `uv run` les pose à
        # la volée, à la version qu'embarque dsoxlab 0.3.1 pour testinfra.
        proc = subprocess.run(
            [
                "uv", "run", "--no-project", "--quiet",
                "--with", "pytest", "--with", "pyyaml", "--with", "pytest-testinfra==10.2.2",
                "python", "-m", "pytest", str(suite), "-q", "--no-header", "-p", "no:cacheprovider",
            ],
            cwd=REPO, env=env, capture_output=True, text=True, check=False,
        )
        resume = proc.stdout.strip().splitlines()
        detail = resume[-1] if resume else f"aucune sortie : {proc.stderr.strip()[-300:]}"
        if avec_solution:
            return proc.returncode == 0, detail
        return re.search(r"\b\d+ passed\b", detail) is None, detail
    except RuntimeError as erreur:
        return False, str(erreur)
    finally:
        try:
            jouer_playbook(lab_rel, "cleanup.yaml", work, etat)
        except RuntimeError as erreur:
            print(f"    cleanup.yaml : {erreur}")
        arreter_services(services)
        if garder:
            print(f"    (répertoire conservé : {tmp})")
        else:
            shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lab", help="ne rejouer qu'un lab (ex: reseau/reseau-prive-scaleway)")
    parser.add_argument("--deux-sens", action="store_true",
                        help="exiger aussi 0 test passé sur l'état de départ")
    parser.add_argument("--check", action="store_true",
                        help="code retour non nul si une solution casse (mode CI)")
    parser.add_argument("--keep", action="store_true",
                        help="conserver les répertoires temporaires pour inspection")
    args = parser.parse_args()

    racine, chiffre = source_des_solutions()
    if not chiffre:
        print(f".vault-pass absent : solutions lues EN CLAIR sous {racine.name}/.")

    versions = {
        "docker": outil_version("docker", "version", "--format", "{{.Server.Version}}"),
        "scw": outil_version("scw", "version"),
        "octl": outil_version("octl", "--version"),
        "incus": outil_version("incus", "version"),
        "ansible-playbook": outil_version("ansible-playbook", "--version"),
    }
    absents = [nom for nom, v in versions.items() if v is None]
    if absents:
        print(f"absent(s) du PATH : {', '.join(absents)}. `mise install` pose scw et "
              "octl ; Docker et Incus doivent répondre.")
        return 1

    labs = [args.lab] if args.lab else solutions_disponibles()
    if not labs:
        print("Aucune solution de référence trouvée.")
        return 0

    outils = ", ".join(f"{n} {v}" for n, v in versions.items())
    print(f"{outils} ; {len(labs)} solution(s) à rejouer.\n")

    resultats: dict[str, dict[str, str]] = {}
    echecs = 0
    for lab_rel in labs:
        print(f"  {lab_rel} ... ", end="", flush=True)
        ok, detail = rejouer(lab_rel, garder=args.keep)
        resultat = {"statut": "ok" if ok else "echec", "detail": detail}
        if args.deux_sens:
            ok_avant, detail_avant = rejouer(lab_rel, garder=args.keep, avec_solution=False)
            resultat["avant"] = detail_avant
            if not ok_avant:
                ok = False
                detail = f"des tests passent AVANT le travail : {detail_avant}"
                resultat.update(statut="echec", detail=detail)
        print("OK" if ok else "ÉCHEC")
        if not ok:
            print(f"    {detail}")
            echecs += 1
        resultats[lab_rel] = resultat

    RECORD.parent.mkdir(parents=True, exist_ok=True)
    RECORD.write_text(json.dumps({
        **versions,
        "verifie_le": datetime.now(UTC).strftime("%Y-%m-%d"),
        "solutions": resultats,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{len(labs) - echecs}/{len(labs)} solution(s) valide(s) avec {outils}.")
    print(f"Résultat enregistré dans {RECORD.relative_to(REPO)}.")
    if echecs and args.check:
        print("\nUne solution ne passe plus : un outil a changé de comportement. "
              "Corrigez la solution ET la leçon correspondante.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
