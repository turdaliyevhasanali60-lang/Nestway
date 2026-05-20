from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.cache import cache
from .models import SiteSettings, Service, BlogPost, ContactLead, AboutPage, NotificationEmail
import resend
import logging

logger = logging.getLogger(__name__)

def site_settings_processor(request):
    site_settings = cache.get('site_settings')
    if site_settings is None:
        site_settings = SiteSettings.load()
        cache.set('site_settings', site_settings, 86400)
    return {
        'site_settings': site_settings
    }

def index(request):
    services = cache.get('index_services')
    if services is None:
        services = list(Service.objects.filter(is_active=True)[:5])
        cache.set('index_services', services, 86400)
        
    latest_posts = cache.get('index_latest_posts')
    if latest_posts is None:
        latest_posts = list(BlogPost.objects.filter(is_published=True)[:3])
        cache.set('index_latest_posts', latest_posts, 86400)
        
    return render(request, 'index.html', {
        'services': services,
        'latest_posts': latest_posts
    })

def services(request):
    services_list = cache.get('active_services')
    if services_list is None:
        services_list = list(Service.objects.filter(is_active=True))
        cache.set('active_services', services_list, 86400)
    return render(request, 'services.html', {'services': services_list})

def about(request):
    about_page = cache.get('about_page')
    if about_page is None:
        about_page = AboutPage.load()
        cache.set('about_page', about_page, 86400)
    return render(request, 'about.html', {'about': about_page})

def service_detail(request, slug):
    cache_key = f'service_detail_{slug}'
    service = cache.get(cache_key)
    if service is None:
        service = get_object_or_404(Service, slug=slug, is_active=True)
        cache.set(cache_key, service, 86400)
        
    other_services_key = f'other_services_{service.id}'
    other_services = cache.get(other_services_key)
    if other_services is None:
        other_services = list(Service.objects.filter(is_active=True).exclude(id=service.id)[:3])
        cache.set(other_services_key, other_services, 86400)
        
    return render(request, 'service_detail.html', {
        'service': service,
        'other_services': other_services
    })

def blog(request):
    posts = cache.get('published_posts')
    if posts is None:
        posts = list(BlogPost.objects.filter(is_published=True))
        cache.set('published_posts', posts, 86400)
    return render(request, 'blog.html', {'posts': posts})

def blog_detail(request, slug):
    cache_key = f'blog_detail_{slug}'
    post = cache.get(cache_key)
    if post is None:
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        cache.set(cache_key, post, 86400)
    return render(request, 'blog_detail.html', {'post': post})

def contact(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        if name and email and message:
            ContactLead.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            
            # Send email via Resend to all active notification recipients
            recipients = list(
                NotificationEmail.objects.filter(is_active=True)
                .values_list('email', flat=True)
            )
            # Fall back to ADMIN_EMAIL env var if no DB recipients configured
            if not recipients and settings.ADMIN_EMAIL:
                recipients = [settings.ADMIN_EMAIL]

            if recipients and settings.RESEND_API_KEY:
                resend.api_key = settings.RESEND_API_KEY
                try:
                    result = resend.Emails.send({
                        "from": settings.RESEND_FROM_EMAIL,
                        "to": recipients,
                        "subject": f"New contact from {name}",
                        "html": (
                            f"<h2>New Contact Form Submission</h2>"
                            f"<p><strong>Name:</strong> {name}</p>"
                            f"<p><strong>Email:</strong> {email}</p>"
                            f"<p><strong>Phone:</strong> {phone or 'N/A'}</p>"
                            f"<p><strong>Message:</strong></p>"
                            f"<p>{message}</p>"
                        ),
                    })
                    logger.info("Resend OK: %s", result)
                except Exception as e:
                    logger.error("Resend failed: %s", e, exc_info=True)
            elif not settings.RESEND_API_KEY:
                logger.warning("RESEND_API_KEY is not set — email not sent.")
            elif not recipients:
                logger.warning("No active notification recipients — email not sent.")
                    
            success = True
            
    return render(request, 'contact.html', {'success': success})
