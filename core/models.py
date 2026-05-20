from django.db import models
from django.utils import timezone

class SiteSettings(models.Model):
    company_name = models.CharField(max_length=255, default="Nestway")
    tagline = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SiteSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Service(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super(Service, self).save(*args, **kwargs)

class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.title} — {self.title}"

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('article', 'Article'),
        ('success_story', 'Success Story'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    body = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='article')
    cover_image = models.ImageField(upload_to='blog/', blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

class ContactLead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"

class NotificationEmail(models.Model):
    """Email addresses that receive contact-form notifications."""
    label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional label, e.g. 'Sales Team' or 'Support Mailbox'"
    )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to temporarily stop sending to this address."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['label', 'email']
        verbose_name = "Notification Email"
        verbose_name_plural = "Notification Emails"

    def __str__(self):
        if self.label:
            return f"{self.label} <{self.email}>"
        return self.email

class AboutPage(models.Model):
    """Singleton model for the About Us page content."""
    hero_title = models.CharField(max_length=255, default="About Nestway")
    hero_subtitle = models.TextField(default="We are a trusted trucking dispatching company dedicated to helping owner-operators and small fleets thrive.")
    mission_title = models.CharField(max_length=255, default="Our Mission")
    mission_body = models.TextField(default="To empower truck drivers and fleet owners with reliable dispatching, transparent pay, and the freedom to be home more often.")
    vision_title = models.CharField(max_length=255, default="Our Vision")
    vision_body = models.TextField(default="A logistics industry where every driver is treated as a partner, not a number.")
    values_title = models.CharField(max_length=255, default="Our Values")
    values_body = models.TextField(default="Integrity, Transparency, Partnership, Excellence.")
    ceo_name = models.CharField(max_length=255, default="Khamidjon Odilov")
    ceo_title = models.CharField(max_length=255, default="Founder & CEO")
    ceo_bio = models.TextField(default="With years of hands-on experience in the Eastern US trucking market, Khamidjon founded Nestway to bring transparency and partnership to an industry that needed it most.")
    ceo_image = models.ImageField(upload_to='about/', blank=True, null=True)
    team_image = models.ImageField(upload_to='about/', blank=True, null=True)
    team_section_title = models.CharField(max_length=255, default="Meet Our Team")
    team_section_body = models.TextField(default="A dedicated group of dispatching professionals committed to your success on the road.")
    stat_1_number = models.CharField(max_length=50, default="92%")
    stat_1_label = models.CharField(max_length=100, default="Customer Satisfaction Rate")
    stat_2_number = models.CharField(max_length=50, default="30+")
    stat_2_label = models.CharField(max_length=100, default="Partner Companies")
    stat_3_number = models.CharField(max_length=50, default="50+")
    stat_3_label = models.CharField(max_length=100, default="Happy Drivers")
    stat_4_number = models.CharField(max_length=50, default="7+")
    stat_4_label = models.CharField(max_length=100, default="Years of Experience")

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return "About Page"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(AboutPage, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
