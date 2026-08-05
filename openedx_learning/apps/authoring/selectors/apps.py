"""
Selectors Django application initialization.
"""

from django.apps import AppConfig


class SelectorsConfig(AppConfig):
    """
    Configuration for the selectors Django application.
    """

    name = "openedx_learning.apps.authoring.selectors"
    verbose_name = "Learning Core > Authoring > Selectors"
    default_auto_field = "django.db.models.BigAutoField"
    label = "oel_selectors"
