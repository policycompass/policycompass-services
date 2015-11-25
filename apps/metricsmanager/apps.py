from django.apps import AppConfig


class metricsmanagerConfig(AppConfig):
    name = 'apps.metricsmanager'
    verbose_name = 'Metricsmanager Manager'

    def ready(self):
        import apps.metricsmanager.signals  # noqa
