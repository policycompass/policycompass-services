from django.apps import AppConfig


class storymanagerConfig(AppConfig):
    name = 'apps.storymanager'
    verbose_name = "Storymanager Manager"

    def ready(self):
        import apps.storymanager.signals  # noqa
