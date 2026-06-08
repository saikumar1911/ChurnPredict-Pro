# File: customers/admin.py



# Import section
from django.contrib import admin
from .models import Customer

# Customer admin registration for the Django admin site.
@admin.register(Customer)
# Class: CustomerAdmin(admin.ModelAdmin)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'risk_level', 'churn_probability', 'created_at']
    list_filter = ['risk_level', 'created_by']
    search_fields = ['name', 'email']
    readonly_fields = ['churn_probability', 'risk_level', 'churn_prediction', 'created_at']
