# File: accounts/churn_system/wsgi.py



"""
WSGI config for churn_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

# Import section
import os

# Import section
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounts.churn_system.settings')

application = get_wsgi_application()
