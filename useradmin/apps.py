from django.apps import AppConfig

class UseradminConfig(AppConfig):
    name = 'useradmin'

    def ready(self):
        import useradmin.signals
