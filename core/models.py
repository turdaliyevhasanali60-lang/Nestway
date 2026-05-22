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
    image_home = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Homepage Image")
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
    LEAD_TYPE_CHOICES = [
        ('general', 'General Contact'),
        ('company_driver', 'Company Driver Application'),
        ('owner_operator', 'Owner Operator Application'),
        ('investor', 'Truck Investor Program'),
        ('academy', 'Truvision Academy Enrollment'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    lead_type = models.CharField(max_length=50, choices=LEAD_TYPE_CHOICES, default='general')
    country = models.CharField(max_length=100, blank=True, null=True)
    experience_level = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

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


class Testimonial(models.Model):
    """Driver testimonials shown on the homepage carousel."""
    quote = models.TextField(help_text="The driver's testimonial text.")
    author_name = models.CharField(max_length=255, help_text="e.g. Marcus T.")
    author_subtitle = models.CharField(max_length=255, blank=True, help_text="e.g. 3 years with Nestway")
    initials = models.CharField(max_length=4, blank=True, help_text="2–4 letter initials shown in the avatar circle, e.g. MT")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.author_name} — {self.author_subtitle}"

    def save(self, *args, **kwargs):
        if not self.initials and self.author_name:
            parts = self.author_name.split()
            self.initials = ''.join(p[0].upper() for p in parts if p)[:4]
        super().save(*args, **kwargs)


class FAQ(models.Model):
    """FAQ items shown in the homepage accordion."""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class USTeamMember(models.Model):
    """US-based staff shown in the USA Office section of the About page."""
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='us_team/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "US Team Member"
        verbose_name_plural = "US Team Members"

    def __str__(self):
        return f"{self.name} — {self.role}"


class Award(models.Model):
    """Logistics awards or accolades won by the company."""
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    year = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    icon_name = models.CharField(
        max_length=50, 
        default='award',
        help_text="Name of icon to display, e.g. 'award', 'shield', 'star', 'truck'"
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Award"
        verbose_name_plural = "Awards"

    def __str__(self):
        return f"{self.title} ({self.year})"


class PartnerReview(models.Model):
    """Testimonials specifically from brokers, shippers, and key partners."""
    quote = models.TextField()
    author_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    relationship = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="e.g. Primary Broker, Major Shipper"
    )
    initials = models.CharField(max_length=4, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Partner Review"
        verbose_name_plural = "Partner Reviews"

    def __str__(self):
        company = f" ({self.company_name})" if self.company_name else ""
        return f"{self.author_name}{company} — {self.relationship}"

    def save(self, *args, **kwargs):
        if not self.initials and self.author_name:
            parts = self.author_name.split()
            self.initials = ''.join(p[0].upper() for p in parts if p)[:4]
        super().save(*args, **kwargs)


class DriverRequirement(models.Model):
    """Hiring requirements shown on the Careers page."""
    DRIVER_TYPE_CHOICES = [
        ('company', 'Company Drivers only'),
        ('owner_operator', 'Owner Operators only'),
        ('both', 'Both categories'),
    ]
    requirement_text = models.CharField(max_length=500)
    driver_type = models.CharField(
        max_length=50,
        choices=DRIVER_TYPE_CHOICES,
        default='both'
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Driver Requirement"
        verbose_name_plural = "Driver Requirements"

    def __str__(self):
        return f"[{self.get_driver_type_display()}] {self.requirement_text}"


