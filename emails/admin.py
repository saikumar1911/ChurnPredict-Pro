# File: emails/admin.py



# Import section
from django.contrib import admin
from .models import EmailLog

# Email log admin page configuration.
@admin.register(EmailLog)
# Class: EmailLogAdmin(admin.ModelAdmin)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['customer', 'subject', 'coupon_code', 'discount_percent', 'sent_at']
    list_filter = ['status', 'sent_at']
