#!/usr/bin/env python3
"""Chiffre les solutions de référence de solution-en-clair/ vers solution/.

Pourquoi ce script existe
-------------------------
Les solutions de ce catalogue ont été écrites et rejouées avant que le mot de
passe du vault (`.vault-pass`) ne soit posé sur le poste. Elles attendent donc,
EN CLAIR, dans `solution-en-clair/`, répertoire ignoré par git. Ce script les
chiffre par `ansible-vault`, fichier par fichier, sous `solution/`, au même
chemin relatif, puis RELIT chaque fichier écrit : un chiffrement qui ne se
déchiffre pas en l'original ne vaut rien.

Il ne supprime jamais `solution-en-clair/` : c'est au formateur de le faire,
une fois `scripts/verify-solutions.py` vert sur les solutions chiffrées.

Usage :
    python3 scripts/chiffrer-solutions.py
    python3 scripts/chiffrer-solutions.py --vault-password-file <fichier> --sortie <rép>
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "solution-en-clair"


def chiffrer(clair: Path, cible: Path, mot_de_passe: Path) -> None:
    cible.parent.mkdir(parents=True, exist_ok=True)
    with open(os.devnull) as entree:
        proc = subprocess.run(
            [
                "ansible-vault", "encrypt", "--vault-password-file", str(mot_de_passe),
                "--output", str(cible), str(clair),
            ],
            stdin=entree, capture_output=True, text=True, check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"{clair.name} : {proc.stderr.strip()}")
        relu = subprocess.run(
            ["ansible-vault", "view", "--vault-password-file", str(mot_de_passe), str(cible)],
            stdin=entree, capture_output=True, check=False,
        )
    if relu.returncode != 0 or relu.stdout != clair.read_bytes():
        raise RuntimeError(f"{cible} ne se déchiffre pas en l'original")
    if not cible.read_text(encoding="utf-8").startswith("$ANSIBLE_VAULT;"):
        raise RuntimeError(f"{cible} n'est pas un fichier vault")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault-password-file", type=Path, default=REPO / ".vault-pass")
    parser.add_argument("--sortie", type=Path, default=REPO / "solution")
    args = parser.parse_args()

    if not args.vault_password_file.is_file():
        print(f"{args.vault_password_file} absent : posez le mot de passe du vault, "
              "puis relancez.", file=sys.stderr)
        return 1
    fichiers = sorted(p for p in SOURCE.rglob("*") if p.is_file())
    if not fichiers:
        print(f"Rien à chiffrer sous {SOURCE.name}/.", file=sys.stderr)
        return 1
    for clair in fichiers:
        cible = args.sortie / clair.relative_to(SOURCE)
        chiffrer(clair, cible, args.vault_password_file)
        print(f"chiffré et relu : {cible.relative_to(args.sortie.parent)}")
    print(f"\n{len(fichiers)} fichier(s) chiffré(s). Rejouez ensuite :\n"
          "    python3 scripts/verify-solutions.py --deux-sens --check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
