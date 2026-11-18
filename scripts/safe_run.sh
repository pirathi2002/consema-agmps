#!/usr/bin/env bash
# Run a command with a hard RAM cap so a heavy script is killed instead of
# freezing the laptop.  Usage: scripts/safe_run.sh [-m 6G] python script.py ...
# (also clears PYTHONPATH so the ROS install does not break pytest/imports)
MEM=8G
if [ "$1" = "-m" ]; then MEM=$2; shift 2; fi
exec systemd-run --user --scope --quiet -p MemoryMax=$MEM -p MemorySwapMax=0 \
     env -u PYTHONPATH "$@"
