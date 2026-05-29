from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StoreManagerProfile

@admin.register(StoreManagerProfile)
class StoreManagerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'phone', 'total_predictions', 'total_emails_sent']