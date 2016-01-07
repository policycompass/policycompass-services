from django.apps import AppConfig


class feedbackmanagerConfig(AppConfig):
    name = 'apps.feedbackmanager'
    verbose_name = "Feedback Manager"

    def ready(self):
        import apps.feedbackmanager.signals  # noqa
