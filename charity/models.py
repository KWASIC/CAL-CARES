from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError

class SiteSettings(models.Model):
    site_title = models.CharField(max_length=100, default='Sadaka')
    site_description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site/', null=True, blank=True)
    favicon = models.ImageField(upload_to='site/', null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    twitter_widget_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.site_title

    class Meta:
        verbose_name_plural = 'Site Settings'

class Cause(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to='causes/')
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to='events/')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE, related_name='donations')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    anonymous = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=100, unique=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.amount}"

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.pk:
            self.cause.raised_amount += self.amount
            self.cause.save()
        super().save(*args, **kwargs)

class HomeCarousel(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='carousel/')
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class AboutSection(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='about/')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Reason(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to='reasons/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="Enter YouTube or Vimeo video URL")
    video_file = models.FileField(upload_to='reason_videos/', blank=True, null=True, 
                                help_text="Upload MP4 video file (max 100MB)")
    order = models.IntegerField(default=0)
    
    def clean(self):
        if self.video_url and self.video_file:
            raise ValidationError("Please provide either a video URL or upload a video file, not both.")
        
        if self.video_file and self.video_file.size > 104857600:  # 100MB in bytes
            raise ValidationError("Video file size must be less than 100MB.")
            
    def get_video_embed_url(self):
        if not self.video_url:
            return None
            
        if 'youtube.com' in self.video_url or 'youtu.be' in self.video_url:
            # Extract YouTube video ID
            if 'youtube.com/watch?v=' in self.video_url:
                video_id = self.video_url.split('watch?v=')[1].split('&')[0]
            elif 'youtu.be/' in self.video_url:
                video_id = self.video_url.split('youtu.be/')[1].split('?')[0]
            else:
                return None
            return f'https://www.youtube.com/embed/{video_id}'
            
        elif 'vimeo.com' in self.video_url:
            # Extract Vimeo video ID
            video_id = self.video_url.split('vimeo.com/')[1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'
            
        return None

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/')
    order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, help_text='Font Awesome class name')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.platform

class Mission(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='mission/')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Program(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='programs/')
    order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class HelpSupport(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome class name (e.g., 'fa-heart')")
    image = models.ImageField(upload_to='help_support/', blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = 'Help & Support Item'
        verbose_name_plural = 'Help & Support Items'
