from django.apps import AppConfig


class LogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.logs"

    def ready(self):
        # Register post_save signals (Lecture 7).
        from . import signals  # noqa: F401
