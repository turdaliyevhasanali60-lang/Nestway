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

ALLOWED_HOSTS = ['nestway-production.up.railway.app', 'nestway-demo-production.up.railway.app', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://nestway-production.up.railway.app', 'https://nestway-demo-production.up.railway.app']

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
DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
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

# Media files — always served from the repo's media/ folder
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Always use local filesystem storage (media files are committed to git)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Resend & Email
RESEND_API_KEY = env('RESEND_API_KEY', default='')
RESEND_FROM_EMAIL = env('RESEND_FROM_EMAIL', default='onboarding@resend.dev')
ADMIN_EMAIL = env('ADMIN_EMAIL', default='')

# Cloudinary (kept for future use, not active)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': env('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default=''),
}

# Caching Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'nestway-cache-storage',
    }
}



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
                        "title": "US Team Members",
                        "icon": "groups",
                        "link": reverse_lazy("admin:core_usteammember_changelist"),
                    },
                    {
                        "title": "Driver Requirements",
                        "icon": "rule",
                        "link": reverse_lazy("admin:core_driverrequirement_changelist"),
                    },
                    {
                        "title": "Awards",
                        "icon": "emoji_events",
                        "link": reverse_lazy("admin:core_award_changelist"),
                    },
                    {
                        "title": "Partner Reviews",
                        "icon": "reviews",
                        "link": reverse_lazy("admin:core_partnerreview_changelist"),
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
