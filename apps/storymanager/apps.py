from django.apps import AppConfig


class datasetmanagerConfig(AppConfig):
    name = 'apps.storymanager'
    verbose_name = "Storymanager Manager"

    def ready(self):
        import apps.storymanager.signals  # noqa