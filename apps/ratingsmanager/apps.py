from django.apps import AppConfig


class RatingsManagerConfig(AppConfig):
    name = 'apps.ratingsmanager'
    verbose_name = 'Ratings Manager'

    def ready(self):
        import apps.ratingsmanager.signals
