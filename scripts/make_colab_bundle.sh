#!/usr/bin/env bash
# Zip the project (code + results + figures, no datasets/venvs) for Google Colab.
#   scripts/make_colab_bundle.sh            -> consema_project.zip (~60 MB, no demo data)
#   scripts/make_colab_bundle.sh --demo     -> also includes demo/ (~210 MB) so the
#                                              viewer runs in Colab without any dataset
set -e
cd "$(dirname "$0")/.."
OUT=../consema_project.zip
rm -f "$OUT"
ITEMS="src experiments tests app scripts notebooks assets pyproject.toml Makefile README.md LICENSE EXTENSION.md results figures"
[ "$1" = "--demo" ] && ITEMS="$ITEMS demo"
zip -qr "$OUT" $ITEMS -x "*/__pycache__/*" "*.egg-info/*" "*/.ipynb_checkpoints/*"
echo "created $(realpath $OUT) ($(du -h $OUT | cut -f1))"
