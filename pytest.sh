#!/bin/bash

BACKLOG_CONFIG=config/local.yaml \
PYTHONPATH="${PYTHONPATH}:$(pwd)/backlog_cli" \
pytest "$@"
