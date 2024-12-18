from django.apps import AppConfig


class NewsConfig(AppConfig):
    verbose_name = 'Публикации'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

