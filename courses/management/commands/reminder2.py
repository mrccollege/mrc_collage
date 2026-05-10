from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'Test if the system is reading this file'

    def handle(self, *args, **options):
        # This will print directly to your terminal
        self.stdout.write(self.style.SUCCESS('SUCCESS: Django is now 2 reading the reminder.py file!'))
        self.stdout.write(f'Current Server Time: {timezone.now()}')
