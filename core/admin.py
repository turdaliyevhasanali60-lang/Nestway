from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin, TabularInline
from .models import SiteSettings, Service, ServiceFeature, BlogPost, ContactLead, AboutPage, NotificationEmail

@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        settings = SiteSettings.load()
        url = reverse('admin:core_sitesettings_change', args=[settings.pk])
        return HttpResponseRedirect(url)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ServiceFeatureInline(TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ('title', 'description', 'order')

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order',)
    inlines = [ServiceFeatureInline]

@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'published_at')
    list_filter = ('category', 'is_published')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ContactLead)
class ContactLeadAdmin(ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
    
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(NotificationEmail)
class NotificationEmailAdmin(ModelAdmin):
    list_display = ('display_name', 'email', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('label', 'email')
    fields = ('label', 'email', 'is_active')

    @admin.display(description='Label / Email')
    def display_name(self, obj):
        return obj.label if obj.label else '—'

@admin.register(AboutPage)
class AboutPageAdmin(ModelAdmin):
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle'),
        }),
        ('Mission, Vision & Values', {
            'fields': ('mission_title', 'mission_body', 'vision_title', 'vision_body', 'values_title', 'values_body'),
        }),
        ('CEO Section', {
            'fields': ('ceo_name', 'ceo_title', 'ceo_bio', 'ceo_image'),
        }),
        ('Team Section', {
            'fields': ('team_section_title', 'team_section_body', 'team_image'),
        }),
        ('Stats', {
            'fields': (
                'stat_1_number', 'stat_1_label',
                'stat_2_number', 'stat_2_label',
                'stat_3_number', 'stat_3_label',
                'stat_4_number', 'stat_4_label',
            ),
        }),
    )

    def changelist_view(self, request, extra_context=None):
        about = AboutPage.load()
        url = reverse('admin:core_aboutpage_change', args=[about.pk])
        return HttpResponseRedirect(url)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
