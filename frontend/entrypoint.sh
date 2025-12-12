#!/usr/bin/env sh
set -e

# Default to development if not explicitly set
APP_ENV="${APP_ENV:-development}"

if [ "$APP_ENV" = "production" ]; then
  npm run build
  exec npm run start
else
  exec npm run dev
fi
