from django.apps import AppConfig


class StoryAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'story_app'

    def ready(self):
        import story_app.signals