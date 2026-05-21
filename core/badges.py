from core.models import ContactLead

def unread_leads_badge(request):
    count = ContactLead.objects.filter(is_read=False).count()
    if count > 0:
        return count
    return None
