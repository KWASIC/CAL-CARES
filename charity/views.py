from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator
from .models import (
    Cause, Event, GalleryImage, HomeCarousel, 
    AboutSection, Reason, Testimonial, Mission, Program, HelpSupport
)
from .forms import ContactForm, DonationForm

def index(request):
    context = {
        'carousel_items': HomeCarousel.objects.all().order_by('order'),
        'featured_causes': Cause.objects.filter(featured=True)[:3],
        'featured_events': Event.objects.filter(featured=True)[:3],
        'reasons': Reason.objects.all().order_by('order')[:4],
        'testimonials': Testimonial.objects.filter(active=True).order_by('order')[:4],
        'missions': Mission.objects.all().order_by('order')[:3],
        'featured_programs': Program.objects.filter(featured=True)[:3],
        'help_support': HelpSupport.objects.all().order_by('order')[:4],
        'donation_form': DonationForm(),
    }
    return render(request, 'charity/index.html', context)

def about(request):
    context = {
        'about_section': AboutSection.objects.first(),
        'testimonials': Testimonial.objects.all()[:4]
    }
    return render(request, 'charity/about.html', context)

def causes(request):
    causes_list = Cause.objects.all()
    paginator = Paginator(causes_list, 9)  # Show 9 causes per page
    page = request.GET.get('page')
    causes = paginator.get_page(page)
    
    context = {
        'causes': causes,
        'is_paginated': causes.has_other_pages(),
        'page_obj': causes,
        'donation_form': DonationForm(),
    }
    return render(request, 'charity/causes.html', context)

def cause_detail(request, slug):
    cause = get_object_or_404(Cause, slug=slug)
    other_causes = Cause.objects.exclude(id=cause.id)[:3]
    donation_form = DonationForm(initial={'cause': cause})
    
    context = {
        'cause': cause,
        'other_causes': other_causes,
        'donation_form': donation_form,
    }
    return render(request, 'charity/cause_detail.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'charity/contact.html', context)

def gallery(request):
    images_list = GalleryImage.objects.all()
    paginator = Paginator(images_list, 12)  # Show 12 images per page
    page = request.GET.get('page')
    gallery_images = paginator.get_page(page)
    
    context = {
        'gallery_images': gallery_images,
        'is_paginated': gallery_images.has_other_pages(),
        'page_obj': gallery_images,
    }
    return render(request, 'charity/gallery.html', context)

def donate(request, cause_id):
    cause = get_object_or_404(Cause, id=cause_id)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.cause = cause
            donation.save()
            cause.raised_amount += donation.amount
            cause.save()
            messages.success(request, 'Thank you for your donation!')
            return redirect('cause_detail', slug=cause.slug)
    return redirect('cause_detail', slug=cause.slug)

class CauseListView(ListView):
    model = Cause
    template_name = 'charity/causes.html'
    context_object_name = 'causes'
    paginate_by = 6

class CauseDetailView(DetailView):
    model = Cause
    template_name = 'charity/cause_detail.html'
    context_object_name = 'cause'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donation_form'] = DonationForm()
        return context

def donate(request, slug):
    cause = get_object_or_404(Cause, slug=slug)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.cause = cause
            donation.save()
            messages.success(request, 'Thank you for your donation!')
            return redirect('cause_detail', slug=slug)
    return redirect('cause_detail', slug=slug)

class EventListView(ListView):
    model = Event
    template_name = 'charity/events.html'
    context_object_name = 'events'
    paginate_by = 6

class EventDetailView(DetailView):
    model = Event
    template_name = 'charity/event_detail.html'
    context_object_name = 'event'

class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'charity/gallery.html'
    context_object_name = 'images'
    paginate_by = 12
