from django.apps import AppConfig

class metricsmanagerConfig(AppConfig):
    name = 'apps.datasetmanager'
    verbose_name = 'Metricsmanager Manager'

    def ready(self):
        import apps.metricsmanager.signals
