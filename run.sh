#!/bin/bash
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
cd "$SCRIPT_DIR" || { echo "[$(date)] Error: Directory not found" >> "$SCRIPT_DIR/error.log"; exit 1; }

# Log all output to a file with timestamps
LOG_FILE="$SCRIPT_DIR/script_$(date +'%Y-%m-%d_%H-%M-%S').log"
exec > >(tee -a "$LOG_FILE") 2>&1
source .venv/bin/activate
python extract.py
python viz.py
