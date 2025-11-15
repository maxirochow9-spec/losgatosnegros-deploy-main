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

echo "-- Ensure static files collected (running collectstatic) --"
python manage.py collectstatic --noinput || echo "collectstatic failed or returned non-zero"

echo "-- staticfiles directory listing --"
if [ -d staticfiles ]; then
  ls -la staticfiles || true
  echo "-- recursive staticfiles listing --"
  find staticfiles -maxdepth 3 -type f -print | sed -n '1,200p' || true
else
  echo "(no staticfiles directory found)"
fi

echo "-- templates directories listing --"
if [ -d tienda/templates ]; then
  find tienda/templates -maxdepth 3 -type f -print | sed -n '1,200p' || true
else
  echo "(no tienda/templates directory found)"
fi

echo "---- starting Gunicorn ----"
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2
