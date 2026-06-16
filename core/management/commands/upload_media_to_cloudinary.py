import os
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files import File

class Command(BaseCommand):
    help = 'Upload local media files to the configured storage backend (e.g., Cloudinary)'

    def handle(self, *args, **options):
        media_root = os.path.join(settings.BASE_DIR, 'media')
        if not os.path.exists(media_root):
            self.stdout.write("Media directory does not exist locally.")
            return

        self.stdout.write("Starting media upload to storage backend...")
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.startswith('.') or file == 'Thumbs.db':
                    continue
                
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, media_root)
                
                # Check if it already exists in the configured storage to save bandwidth/time
                try:
                    if default_storage.exists(relative_path):
                        self.stdout.write(f"Skipping {relative_path} (already exists in storage)")
                        continue
                except Exception as e:
                    self.stdout.write(f"Checking existence failed for {relative_path}, attempting upload: {e}")

                self.stdout.write(f"Uploading {relative_path}...")
                try:
                    with open(local_path, 'rb') as f:
                        django_file = File(f)
                        default_storage.save(relative_path, django_file)
                    self.stdout.write(self.style.SUCCESS(f"Successfully uploaded {relative_path}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Failed to upload {relative_path}: {e}"))
        self.stdout.write(self.style.SUCCESS("Media upload process completed."))
