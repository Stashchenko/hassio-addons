#!/usr/bin/env bash
set -e

PORT="${EQ_WEB_PORT:-1706}"

export PYTHONPATH=/usr/web
exec waitress-serve --host=0.0.0.0 --port="${PORT}" app:app
