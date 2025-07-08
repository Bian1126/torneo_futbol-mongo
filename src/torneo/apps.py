from django.apps import AppConfig

class TorneoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'torneo'

    def ready(self):
        import torneo.signals

