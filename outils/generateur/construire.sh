#!/usr/bin/env bash
# Reconstruit le site dans site/ à partir de contenu/ (lancé par Netlify à chaque envoi, et par le contrôle GitHub).
# Les images, vidéos, polices et modèles 3D sont déjà dans site/ : seules les pages et les photos ajoutées par /admin sont régénérées.
set -euo pipefail
cd "$(dirname "$0")"
ln -sfn ../../site out
"${PYTHON:-python3}" build.py
