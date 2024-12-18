from django.core.management.base import BaseCommand
import keyboard
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Hello')
        os.system("python manage.py custom_run")
        keyboard.press_and_release('Ctrl+Shift+T')
        os.system("celery -A NewsPaper worker -l INFO --pool=solo")
