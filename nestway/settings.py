"""
Django settings for nestway project.
"""

from pathlib import Path
import environ
import os
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Read .env file if it exists
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), overwrite=True)

# Quick-start development settings - unsuitable for production
SECRET_KEY = env('SECRET_KEY', default='django-insecure-default-key')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['nestway-demo-production.up.railway.app', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://nestway-demo-production.up.railway.app']

# Application definition
INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nestway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.views.site_settings_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'nestway.wsgi.application'

# Database
if DEBUG:
    DATABASES = {
        'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
    }
else:
    # In production, always use the persistent volume path regardless of DATABASE_URL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/app/data/db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
if DEBUG:
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    MEDIA_ROOT = '/app/data/media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Resend & Email
RESEND_API_KEY = env('RESEND_API_KEY', default='')
RESEND_FROM_EMAIL = env('RESEND_FROM_EMAIL', default='onboarding@resend.dev')
ADMIN_EMAIL = env('ADMIN_EMAIL', default='')

# Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': env('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default=''),
}

# Use local media storage in development, Cloudinary in production
if DEBUG:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Caching Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'nestway-cache-storage',
    }
}

# Auto-restore SQLite database and media files on first startup in production
if not DEBUG:
    import os
    import sys
    import shutil

    # Skip during collectstatic to avoid unnecessary copying in the build phase
    if 'collectstatic' not in sys.argv:
        db_path = '/app/data/db.sqlite3'
        source_db = os.path.join(BASE_DIR, 'db.sqlite3')
        force_restore = os.environ.get('FORCE_RESTORE_DB', 'False').lower() in ('true', '1', 'yes')

        # 1. Database restoration
        # Check if the database in the persistent volume is empty of our data (e.g. 0 services)
        is_empty = True
        if os.path.exists(db_path) and os.path.getsize(db_path) > 0:
            try:
                import sqlite3
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM core_service;")
                count = cursor.fetchone()[0]
                if count > 0:
                    is_empty = False
                conn.close()
            except Exception:
                # If table doesn't exist or query fails, it's considered empty/uninitialized
                is_empty = True

        if not os.path.exists(db_path) or os.path.getsize(db_path) == 0 or is_empty or force_restore:
            print(f"[DB Restore] Copying database from git-tracked db.sqlite3 to {db_path} (is_empty={is_empty}, force={force_restore})...")
            try:
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                if os.path.exists(source_db):
                    shutil.copy2(source_db, db_path)
                    print("[DB Restore] Database copied successfully.")
                else:
                    print(f"[DB Restore] Source DB {source_db} not found!")
            except Exception as e:
                print(f"[DB Restore] Error copying database: {e}")

        # 2. Media files synchronization
        media_dest = '/app/data/media'
        source_media = os.path.join(BASE_DIR, 'media')

        if os.path.exists(source_media):
            print(f"[Media Restore] Synchronizing media files to {media_dest}...")
            try:
                os.makedirs(media_dest, exist_ok=True)
                for root, dirs, files in os.walk(source_media):
                    for file in files:
                        src_file = os.path.join(root, file)
                        rel_path = os.path.relpath(src_file, source_media)
                        dest_file = os.path.join(media_dest, rel_path)
                        
                        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                        if not os.path.exists(dest_file) or force_restore:
                            shutil.copy2(src_file, dest_file)
                print("[Media Restore] Media files synchronized successfully.")
            except Exception as e:
                print(f"[Media Restore] Error copying media files: {e}")

UNFOLD = {
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Core",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Contact leads",
                        "icon": "mail",
                        "link": reverse_lazy("admin:core_contactlead_changelist"),
                        "badge": "core.badges.unread_leads_badge",
                    },
                    {
                        "title": "About Page",
                        "icon": "info",
                        "link": reverse_lazy("admin:core_aboutpage_changelist"),
                    },
                    {
                        "title": "Blog posts",
                        "icon": "article",
                        "link": reverse_lazy("admin:core_blogpost_changelist"),
                    },
                    {
                        "title": "FAQs",
                        "icon": "help",
                        "link": reverse_lazy("admin:core_faq_changelist"),
                    },
                    {
                        "title": "Notification Emails",
                        "icon": "mark_email_read",
                        "link": reverse_lazy("admin:core_notificationemail_changelist"),
                    },
                    {
                        "title": "Services",
                        "icon": "build",
                        "link": reverse_lazy("admin:core_service_changelist"),
                    },
                    {
                        "title": "Site Settings",
                        "icon": "settings",
                        "link": reverse_lazy("admin:core_sitesettings_changelist"),
                    },
                    {
                        "title": "Testimonials",
                        "icon": "star",
                        "link": reverse_lazy("admin:core_testimonial_changelist"),
                    },
                ],
            },
            {
                "title": "Authentication and Authorization",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Groups",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
        ],
    },
}
