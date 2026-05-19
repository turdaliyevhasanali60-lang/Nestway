import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nestway.settings')
django.setup()

from core.models import Service

for service in Service.objects.all():
    if not service.slug:
        service.slug = slugify(service.title)
        service.save()
print("Slugs updated")
