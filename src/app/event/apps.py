from django.apps import AppConfig


class EventConfig(AppConfig):
    name = "app.event"
    verbose_name = "06.행사"

    def ready(self):
        import app.event.signals
