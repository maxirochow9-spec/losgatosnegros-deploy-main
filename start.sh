#!/usr/bin/env bash
set -euo pipefail

echo "---- start.sh: starting boot diagnostics ----"
echo "Date: $(date)"

echo "-- Procfile (repo root) --"
if [ -f Procfile ]; then
  cat Procfile
else
  echo "(no Procfile found)"
fi

echo "-- Python info --"
which python || true
python -V || true

echo "-- Gunicorn info --"
which gunicorn || true
gunicorn --version || true

echo "-- DJANGO settings module --"
# Avoid unbound variable when running with `set -u`.
# Use the existing env var if set, otherwise default to `core.settings`.
DJANGO_SETTINGS_MODULE_VALUE="${DJANGO_SETTINGS_MODULE:-core.settings}"
echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE_VALUE}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE_VALUE}"

echo "-- Relevant env vars (filtered) --"
env | grep -i "DJANGO\|SECRET_KEY\|POSTGRES\|SUPABASE\|RENDER" || true

echo "-- Listing project root --"
ls -la || true

echo "---- starting Gunicorn ----"
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2
