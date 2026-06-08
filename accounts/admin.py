# File: accounts/admin.py



# Import section
from django.contrib import admin
from .models import StoreManagerProfile

# Admin configuration for store manager profile data.
@admin.register(StoreManagerProfile)
# Class: StoreManagerProfileAdmin(admin.ModelAdmin)
class StoreManagerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'phone', 'total_predictions', 'total_emails_sent']
