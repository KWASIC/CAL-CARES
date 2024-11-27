from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('causes/', views.causes, name='causes'),
    path('causes/<slug:slug>/', views.cause_detail, name='cause_detail'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('donate/<int:cause_id>/', views.donate, name='donate'),
]
