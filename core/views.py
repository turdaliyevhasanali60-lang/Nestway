from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import SiteSettings, Service, BlogPost, ContactLead, AboutPage, NotificationEmail
import resend
import logging

logger = logging.getLogger(__name__)

def site_settings_processor(request):
    return {
        'site_settings': SiteSettings.load()
    }

def index(request):
    services = Service.objects.filter(is_active=True)[:5]
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    return render(request, 'index.html', {
        'services': services,
        'latest_posts': latest_posts
    })

def services(request):
    services_list = Service.objects.filter(is_active=True)
    return render(request, 'services.html', {'services': services_list})

def about(request):
    about_page = AboutPage.load()
    return render(request, 'about.html', {'about': about_page})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    other_services = Service.objects.filter(is_active=True).exclude(id=service.id)[:3]
    return render(request, 'service_detail.html', {
        'service': service,
        'other_services': other_services
    })

def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
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
