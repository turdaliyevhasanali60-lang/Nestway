from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        import core.signals

        # Only run in production (when not in DEBUG)
        from django.conf import settings
        if not settings.DEBUG:
            import os
            import sys
            import shutil

            # Skip during collectstatic to avoid unnecessary copying in build container
            if 'collectstatic' in sys.argv:
                return

            db_path = settings.DATABASES['default']['NAME']
            source_db = os.path.join(settings.BASE_DIR, 'db.sqlite3')
            force_restore = os.environ.get('FORCE_RESTORE_DB', 'False').lower() in ('true', '1', 'yes')

            # 1. Handle SQLite DB restoring/copying
            # Only copy if the database doesn't exist, is empty, or FORCE_RESTORE_DB is True
            if not os.path.exists(db_path) or os.path.getsize(db_path) == 0 or force_restore:
                print(f"[DB Restore] Copying from git-tracked db.sqlite3 to {db_path}...")
                try:
                    os.makedirs(os.path.dirname(db_path), exist_ok=True)
                    if os.path.exists(source_db):
                        shutil.copy2(source_db, db_path)
                        print("[DB Restore] Database copied successfully.")
                    else:
                        print(f"[DB Restore] Source DB {source_db} not found!")
                except Exception as e:
                    print(f"[DB Restore] Error copying database: {e}")

            # 2. Handle Media Files restoring/copying
            media_dest = settings.MEDIA_ROOT
            source_media = os.path.join(settings.BASE_DIR, 'media')

            if os.path.exists(source_media):
                print(f"[Media Restore] Synchronizing media files to {media_dest}...")
                try:
                    os.makedirs(media_dest, exist_ok=True)
                    # We copy all subdirectories and files
                    for root, dirs, files in os.walk(source_media):
                        for file in files:
                            src_file = os.path.join(root, file)
                            rel_path = os.path.relpath(src_file, source_media)
                            dest_file = os.path.join(media_dest, rel_path)
                            
                            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                            # Copy if the destination file doesn't exist or if force_restore is True
                            if not os.path.exists(dest_file) or force_restore:
                                shutil.copy2(src_file, dest_file)
                    print("[Media Restore] Media files synchronized successfully.")
                except Exception as e:
                    print(f"[Media Restore] Error copying media files: {e}")
