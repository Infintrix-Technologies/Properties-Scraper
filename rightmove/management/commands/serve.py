import subprocess
import threading
from django.core.management.base import BaseCommand
from rightmove.models import Area
from rightmove.tasks import scrape_properties


class Command(BaseCommand):
    help = "Run multiple commands in parallel"

    def handle(self, *args, **options):
        # Define the commands to run in parallel
        commands = [
            "python manage.py makemigrations && python manage.py migrate",
            "python manage.py runserver 0.0.0.0:8000",
            "redis-server",
            "celery -A core worker -l INFO",
            "celery -A core beat --loglevel=info",
        ]

        # Function to run a command in a separate thread
        self.create_areas()

        def run_command(command):
            subprocess.call(command, shell=True)

        threads = []

        # Start a separate thread for each command
        for command in commands:
            thread = threading.Thread(target=run_command, args=(command,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        self.stdout.write(
            self.style.SUCCESS("All commands have been executed in parallel.")
        )

    def create_areas(self):
        areas_to_create = [
            ("Amber Valley", "DE5"),
            ("Ashfield", "NG17"),
            ("Bassetlaw", "DN22"),
            ("Birmingham", "B1"),
            ("Blaby", "LE8"),
            ("Bolsover", "S44"),
            ("Boston", "PE21"),
        ]

        for name, zip_code in areas_to_create:
            # Check if an area with the given name and zip code already exists
            existing_area = Area.objects.filter(name=name, zip=zip_code).first()

            if not existing_area:
                # If the area does not exist, create a new one
                new_area = Area(name=name, zip=zip_code)
                new_area.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created area: {new_area}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Area already exists: {existing_area}")
                )

        
