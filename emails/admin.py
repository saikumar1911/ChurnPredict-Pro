from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EmailLog

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['customer', 'subject', 'coupon_code', 'discount_percent', 'sent_at']
    list_filter = ['status', 'sent_at']