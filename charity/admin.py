from django.contrib import admin
from .models import (
    SiteSettings, Cause, Event, GalleryImage, ContactMessage,
    Donation, HomeCarousel, AboutSection, Reason, Testimonial,
    SocialLink, Mission, Program, HelpSupport
)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'email', 'phone')

@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal_amount', 'raised_amount', 'featured', 'created_at')
    list_filter = ('featured', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'featured', 'created_at')
    list_filter = ('featured', 'date', 'created_at')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'amount', 'cause', 'created_at', 'anonymous')
    list_filter = ('anonymous', 'created_at')
    search_fields = ('name', 'email', 'message')

@admin.register(HomeCarousel)
class HomeCarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'has_image', 'has_video')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'order')
        }),
        ('Media', {
            'fields': ('image', ('video_url', 'video_file')),
            'description': 'Add either an image, a video URL (YouTube/Vimeo), or upload a video file.'
        })
    )
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
    
    def has_video(self, obj):
        return bool(obj.video_url or obj.video_file)
    has_video.boolean = True
    has_video.short_description = 'Has Video'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'active')
    list_editable = ('order', 'active')
    search_fields = ('name', 'position', 'content')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order')
    list_editable = ('order',)

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'order')
    list_editable = ('featured', 'order')

@admin.register(HelpSupport)
class HelpSupportAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'content')
    fields = ('title', 'content', 'icon', 'image', 'order')
