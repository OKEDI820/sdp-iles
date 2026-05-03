"""Production settings — security hardening."""
from .base import *  # noqa: F401,F403

DEBUG = False

# Use a real SMTP backend in production. Configure via env vars.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "")  # noqa: F405
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))  # noqa: F405
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")  # noqa: F405
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")  # noqa: F405

# Security headers — Lecture 4 best practices.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
