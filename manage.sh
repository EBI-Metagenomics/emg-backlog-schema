#!/bin/bash

PYTHONPATH="${PYTHONPATH}:$(pwd)/backlog_cli" \
BACKLOG_CONFIG=config/local.yaml \
python backlog_cli/manage.py "$@"
