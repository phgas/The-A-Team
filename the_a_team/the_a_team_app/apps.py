from django.apps import AppConfig


class The_A_Team_AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_a_team_app'
    def ready(self):
        import the_a_team_app.signals
