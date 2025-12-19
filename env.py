"""
Local environment variables for the project.

Place secrets and environment-specific settings here. This file is
imported by `taskmaster/settings.py`. Do NOT commit production
secrets to a public repository.
"""

import os

os.environ.setdefault("DEBUG", "True")

# Django SECRET_KEY for local development. Replace with a secure key
# for production. Use `os.environ.setdefault` so running processes
# will populate the environment variable when this file is imported.
SECRET_KEY = os.environ.setdefault(
    'SECRET_KEY', 'django-insecure-hx3&lq9z!u7b2c5k1m0p@r8v4s6n#y2d'
)

# Local Postgres connection string (optional). Example:
# postgres://USER:PASSWORD@HOST:PORT/DBNAME
# Set this to an empty string here for development, or export
# the DATABASE_URL environment variable (used in production like Heroku).
DATABASE_URL = os.environ.setdefault(
    'DATABASE_URL', '''postgresql://neondb_owner:npg_dDkAKtP9w0ue@ep-rough-
heart-ag1orf0v.c-2.eu-central-1.aws.neon.tech/brick_aqua_bunch_899292'''
)
