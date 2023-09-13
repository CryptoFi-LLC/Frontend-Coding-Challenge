#!/bin/sh

python docker/scripts/run_api_server.py

exec "$@"