from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import SiteSettings, AboutPage, Service, ServiceFeature, BlogPost, Testimonial, FAQ

@receiver(post_save, sender=SiteSettings)
@receiver(post_delete, sender=SiteSettings)
@receiver(post_save, sender=AboutPage)
@receiver(post_delete, sender=AboutPage)
@receiver(post_save, sender=Service)
@receiver(post_delete, sender=Service)
@receiver(post_save, sender=ServiceFeature)
@receiver(post_delete, sender=ServiceFeature)
@receiver(post_save, sender=BlogPost)
@receiver(post_delete, sender=BlogPost)
@receiver(post_save, sender=Testimonial)
@receiver(post_delete, sender=Testimonial)
@receiver(post_save, sender=FAQ)
@receiver(post_delete, sender=FAQ)
def clear_site_cache(sender, **kwargs):
    cache.clear()
