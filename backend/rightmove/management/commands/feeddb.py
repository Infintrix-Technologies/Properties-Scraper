import subprocess
import threading
from django.core.management.base import BaseCommand
from rightmove.models import Area
from rightmove.tasks import scrape_properties
from django.contrib.auth.models import User
from django.core.management import call_command


class Command(BaseCommand):
    help = "Run multiple commands in parallel"

    def handle(self, *args, **options):
        # Define the commands to run in parallel
        self.create_areas()
        self.create_superuser()

    def create_superuser(self):
        # Check if the superuser already exists
        if not User.objects.filter(username="admin").exists():
            user = User()
            user.username = "admin"
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.set_password = "1234"
            user.save()
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists."))

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
