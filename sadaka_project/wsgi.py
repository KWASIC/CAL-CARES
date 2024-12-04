"""
WSGI config for sadaka_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Add project directory to Python path
path = '/home/Calvin31/CAL-CARES'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'sadaka_project.settings'
os.environ['PAYSTACK_PUBLIC_KEY'] = 'pk_live_55ef871debbd9948a6fb282b39b2dd5404fabf56'
os.environ['PAYSTACK_SECRET_KEY'] = 'sk_live_4d2f5e2f7f9e070df5c6aa9e0c4e5e1f0c0d0b0a'

# Initialize WSGI application
application = get_wsgi_application()
