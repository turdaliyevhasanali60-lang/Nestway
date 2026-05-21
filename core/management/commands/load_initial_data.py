import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from core.models import Service, SiteSettings

class Command(BaseCommand):
    help = 'Load initial data from JSON fixture if the database is empty'

    def handle(self, *args, **options):
        # We check if SiteSettings or Services already exist in the database.
        # If they do, we assume the database is already populated and skip loading to avoid overwriting edits.
        if SiteSettings.objects.exists() or Service.objects.exists():
            self.stdout.write(self.style.WARNING("Database already has data. Skipping initial data load to preserve updates."))
            return

        fixture_path = 'datadump.json'
        if os.path.exists(fixture_path):
            self.stdout.write(self.style.MIGRATE_LABEL(f"Loading initial data from {fixture_path}..."))
            try:
                call_command('loaddata', fixture_path)
                self.stdout.write(self.style.SUCCESS("Successfully loaded initial database data."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error loading fixture: {e}"))
        else:
            self.stdout.write(self.style.WARNING(f"Fixture file {fixture_path} not found. Skipping load."))
