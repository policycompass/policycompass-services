from django.apps import AppConfig

class metricsmanagerConfig(AppConfig):
    name = 'apps.metricsmanager'
    verbose_name = "Metrics Manager"

    def ready(self):
        import apps.metricsmanager.signals

