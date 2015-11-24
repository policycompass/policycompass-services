from django.apps import AppConfig


class datasetmanagerConfig(AppConfig):
    name = 'apps.datasetmanager'
    verbose_name = "Datasetmanager Manager"

    def ready(self):
        import apps.datasetmanager.signals  # noqa
