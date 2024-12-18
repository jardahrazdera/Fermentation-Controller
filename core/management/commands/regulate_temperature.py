from django.core.management.base import BaseCommand
from core.controllers import regulate_temperature

class Command(BaseCommand):
    help = "Regulates temperature for all tanks by controlling valves"

    def handle(self, *args, **options):
        self.stdout.write("Starting temperature regulation...")
        regulate_temperature()
        self.stdout.write("Temperature regulation completed successfully.")
