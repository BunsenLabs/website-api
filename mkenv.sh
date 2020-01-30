#!/usr/bin/env bash
set -e

SCRIPTDIR=$(cd "$(dirname -- "$0")" && pwd)

python -m venv "$SCRIPTDIR"/.env
source "$SCRIPTDIR"/.env/bin/activate

pip install --upgrade -r "$SCRIPTDIR"/requirements.txt

exit 0
