from django.apps import AppConfig


class AGManagerConfig(AppConfig):
    name = 'apps.agmanager'
    verbose_name = "Argumentation Graph Manager"

    def ready(self):
        import apps.agmanager.signals  # noqa
