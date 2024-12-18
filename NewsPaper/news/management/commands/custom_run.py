from django.core.management.base import BaseCommand
import keyboard
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Hello')
        os.system("celery -A NewsPaper worker -l INFO --pool-solo")

        # keyboard.press_and_release("Enter")

        keyboard.press_and_release('Ctrl+Shift+T')
        os.system("python manage.py runserver")
        # keyboard.press_and_release("Enter")