from .models import SiteSettings, SocialLink

def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
        social_links = SocialLink.objects.all()
    except:
        settings = None
        social_links = []
    
    return {
        'site_settings': settings,
        'social_links': social_links,
    }
