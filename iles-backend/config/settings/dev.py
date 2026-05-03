"""Development settings — console email, permissive CORS for Vite."""
from .base import *  # noqa: F401,F403

DEBUG = True

# Lecture 7: emails print to runserver console in dev.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# In dev we let Vite hit us from anywhere on localhost.
CORS_ALLOW_ALL_ORIGINS = True
