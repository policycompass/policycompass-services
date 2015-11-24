from django.apps import AppConfig


class indicatorserviceConfig(AppConfig):
    name = 'apps.indicatorservice'
    verbose_name = "Indicator Service"

    def ready(self):
        import apps.indicatorservice.signals  # noqa
