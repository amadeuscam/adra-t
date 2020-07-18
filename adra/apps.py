from django.apps import AppConfig


class AdraConfig(AppConfig):
    name = 'adra'

    def ready(self):
        import adra.signals
