#!/bin/bash
pwd
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1
source .venv/bin/activate
python extract.py load
python viz.py plot
