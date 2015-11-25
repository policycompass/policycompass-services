from django.apps import AppConfig


class visualizationsmanagerConfig(AppConfig):
    name = 'apps.visualizationsmanager'
    verbose_name = "Visualizations Manager"

    def ready(self):
        import apps.visualizationsmanager.signals  # noqa
