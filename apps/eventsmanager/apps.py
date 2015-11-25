from django.apps import AppConfig


class eventsmanagerConfig(AppConfig):
    name = 'apps.eventsmanager'
    verbose_name = "Events Manager"

    def ready(self):
        import apps.eventsmanager.signals  # noqa
