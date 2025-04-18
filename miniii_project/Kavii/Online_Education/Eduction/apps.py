from django.apps import AppConfig


class EductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Eduction'
    
    def ready(self):
        import Eduction.signals
