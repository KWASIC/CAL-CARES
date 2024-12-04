from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.db.models import Sum
from django.core.paginator import Paginator
from .models import (
    Cause, Event, GalleryImage, HomeCarousel, 
    AboutSection, Reason, Testimonial, Mission, Program, HelpSupport, Donation
)
from .forms import ContactForm, DonationForm
from .utils.payment import PaystackAPI
import uuid
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

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

def donate(request, cause_id=None, slug=None):
    if slug:
        cause = get_object_or_404(Cause, slug=slug)
    else:
        cause = get_object_or_404(Cause, id=cause_id)
        
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.cause = cause
            donation.save()
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

@require_http_methods(["POST"])
@ensure_csrf_cookie
def process_donation(request, cause_id):
    try:
        # Log request details for debugging
        print(f"Processing donation for cause {cause_id}")
        print(f"Request method: {request.method}")
        print(f"Headers: {request.headers}")
        
        cause = get_object_or_404(Cause, id=cause_id)
        amount = float(request.POST.get('amount', 0))
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        message = request.POST.get('message', '')
        anonymous = request.POST.get('anonymous') == 'on'
        
        # Validate required fields
        if not amount or amount <= 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Please enter a valid amount'
            }, status=400)
            
        if not email:
            return JsonResponse({
                'status': 'error',
                'message': 'Please enter your email address'
            }, status=400)
            
        if not name:
            return JsonResponse({
                'status': 'error',
                'message': 'Please enter your name'
            }, status=400)
        
        # Generate unique reference
        reference = f"don_{uuid.uuid4().hex[:10]}"
        
        # Create donation record
        donation = Donation.objects.create(
            cause=cause,
            name=name,
            email=email,
            amount=amount,
            message=message,
            anonymous=anonymous,
            payment_reference=reference,
            status='pending'
        )
        
        # Initialize Paystack payment
        paystack = PaystackAPI()
        callback_url = request.build_absolute_uri(
            reverse('verify_donation', args=[donation.id])
        )
        
        try:
            payment_url = paystack.get_payment_url(
                email=email,
                amount=amount,
                reference=reference,
                callback_url=callback_url
            )
            return JsonResponse({
                'status': 'success',
                'payment_url': payment_url
            })
        except Exception as e:
            print(f"Paystack error: {str(e)}")
            donation.status = 'failed'
            donation.save()
            return JsonResponse({
                'status': 'error',
                'message': 'Unable to initialize payment. Please try again.'
            }, status=400)
            
    except Exception as e:
        print(f"Process donation error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred. Please try again.'
        }, status=500)

def initiate_donation(request, cause_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    try:
        cause = Cause.objects.get(id=cause_id)
        amount = float(request.POST.get('amount'))
        email = request.POST.get('email')
        name = request.POST.get('name')
        
        # Generate unique reference
        reference = f"don_{uuid.uuid4().hex[:10]}"
        
        # Save pending donation
        donation = Donation.objects.create(
            cause=cause,
            name=name,
            email=email,
            amount=amount,
            payment_reference=reference,
            status='pending'
        )
        
        # Initialize Paystack payment
        paystack = PaystackAPI()
        callback_url = request.build_absolute_uri(
            reverse('verify_donation', args=[donation.id])
        )
        
        try:
            payment_url = paystack.get_payment_url(
                email=email,
                amount=amount,
                reference=reference,
                callback_url=callback_url
            )
            return JsonResponse({
                'status': 'success',
                'payment_url': payment_url
            })
        except Exception as e:
            donation.status = 'failed'
            donation.save()
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
            
    except Cause.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Cause not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def verify_donation(request, donation_id):
    try:
        donation = get_object_or_404(Donation, id=donation_id)
        
        # Only verify pending donations
        if donation.status != 'pending':
            messages.warning(request, 'This donation has already been processed')
            return redirect('cause_detail', slug=donation.cause.slug)
            
        paystack = PaystackAPI()
        
        # Verify the payment
        try:
            response = paystack.verify_payment(donation.payment_reference)
            
            if response['status'] and response['data']['status'] == 'success':
                # Update donation status
                donation.status = 'completed'
                donation.save()
                
                messages.success(request, 'Thank you for your donation!')
            else:
                donation.status = 'failed'
                donation.save()
                messages.error(request, 'Payment verification failed')
                
        except Exception as e:
            donation.status = 'failed'
            donation.save()
            messages.error(request, str(e))
            
        return redirect('cause_detail', slug=donation.cause.slug)
        
    except Donation.DoesNotExist:
        messages.error(request, 'Donation not found')
        return redirect('home')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('home')
