from django.apps import AppConfig


class AuthorAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'author_app'

    def ready(self):
        import author_app.signals