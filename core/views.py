from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.cache import cache
from .models import (
    SiteSettings, Service, BlogPost, ContactLead, AboutPage, NotificationEmail, Testimonial, FAQ,
    USTeamMember, Award, PartnerReview, DriverRequirement
)
from .telegram_bot import send_telegram_lead
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
        cache.set('index_latest_posts', latest_posts, 300)  # 5 min — refreshes quickly after new posts

    testimonials = cache.get('active_testimonials')
    if testimonials is None:
        testimonials = list(Testimonial.objects.filter(is_active=True))
        cache.set('active_testimonials', testimonials, 3600)

    faqs = cache.get('active_faqs')
    if faqs is None:
        faqs = list(FAQ.objects.filter(is_active=True))
        cache.set('active_faqs', faqs, 3600)

    return render(request, 'index.html', {
        'services': services,
        'latest_posts': latest_posts,
        'testimonials': testimonials,
        'faqs': faqs,
    })

def services(request):
    services_list = cache.get('active_services')
    if services_list is None:
        services_list = list(Service.objects.filter(is_active=True))
        cache.set('active_services', services_list, 3600)  # 1 hour
    return render(request, 'services.html', {'services': services_list})

def about(request):
    about_page = cache.get('about_page')
    if about_page is None:
        about_page = AboutPage.load()
        cache.set('about_page', about_page, 86400)

    # Fetch active US team members
    us_team = list(USTeamMember.objects.filter(is_active=True).order_by('order'))

    return render(request, 'about.html', {
        'about': about_page,
        'us_team': us_team,
    })

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
        cache.set('published_posts', posts, 300)  # 5 min — new posts appear quickly
    success_stories = [p for p in posts if p.category == 'success_story']
    articles = [p for p in posts if p.category == 'article']
    return render(request, 'blog.html', {
        'success_stories': success_stories,
        'articles': articles
    })

def blog_detail(request, slug):
    cache_key = f'blog_detail_{slug}'
    post = cache.get(cache_key)
    if post is None:
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        cache.set(cache_key, post, 300)  # 5 min
    return render(request, 'blog_detail.html', {'post': post})

def contact(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        if name and email and message:
            lead = ContactLead.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message,
                lead_type='general'
            )
            
            # Send Telegram Bot notification
            send_telegram_lead(lead)
            
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


def careers(request):
    success = False
    active_tab = 'company'
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        lead_type = request.POST.get('lead_type', 'company_driver')
        experience_level = request.POST.get('experience_level', '')
        message = request.POST.get('message', '')
        
        if name and email:
            lead = ContactLead.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message,
                lead_type=lead_type,
                experience_level=experience_level
            )
            
            # Send Telegram Bot notification
            send_telegram_lead(lead)
            
            success = True
            if lead_type == 'company_driver':
                active_tab = 'company'
            elif lead_type == 'owner_operator':
                active_tab = 'owner'
            elif lead_type == 'investor':
                active_tab = 'investor'
                
    # Fetch active driver requirements
    requirements = list(DriverRequirement.objects.filter(is_active=True).order_by('order'))
    company_requirements = [r for r in requirements if r.driver_type in ['company', 'both']]
    owner_requirements = [r for r in requirements if r.driver_type in ['owner_operator', 'both']]
    
    return render(request, 'careers.html', {
        'success': success,
        'active_tab': active_tab,
        'company_requirements': company_requirements,
        'owner_requirements': owner_requirements,
    })


def truvision(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        country = request.POST.get('country', '')
        experience_level = request.POST.get('experience_level', '')
        message = request.POST.get('message', '')
        
        if name and email:
            lead = ContactLead.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message,
                lead_type='academy',
                country=country,
                experience_level=experience_level
            )
            
            # Send Telegram Bot notification
            send_telegram_lead(lead)
            
            success = True
            
    return render(request, 'truvision.html', {'success': success})


def awards(request):
    awards_list = list(Award.objects.filter(is_active=True).order_by('order'))
    partner_reviews = list(PartnerReview.objects.filter(is_active=True).order_by('order'))
    
    return render(request, 'awards.html', {
        'awards': awards_list,
        'partner_reviews': partner_reviews,
    })
