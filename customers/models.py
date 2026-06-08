# File: customers/models.py



# Import section
from django.db import models
from django.contrib.auth.models import User

# Customer data model used by the churn prediction system.
class Customer(models.Model):
    RISK_CHOICES = [
        ('High', '🔴 High Risk'),
        ('Medium', '🟡 Medium Risk'),
        ('Low', '🟢 Low Risk'),
    ]

    # ----------------------------
    # Basic customer information
    # ----------------------------
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)

    # ----------------------------
    # Prediction feature fields
    # ----------------------------
    total_orders = models.IntegerField(default=0)
    total_spent = models.FloatField(default=0)
    days_since_last_order = models.IntegerField(default=0)
    complaint_count = models.IntegerField(default=0)
    tenure = models.IntegerField(default=0)
    city_tier = models.IntegerField(default=1)
    warehouse_to_home = models.IntegerField(default=0)
    preferred_payment_mode = models.CharField(max_length=50, blank=True, default='')
    gender = models.CharField(max_length=10, blank=True, default='')
    hour_spend_on_app = models.IntegerField(default=2)
    number_of_device_registered = models.IntegerField(default=1)
    preferred_order_cat = models.CharField(max_length=50, blank=True, default='')
    satisfaction_score = models.IntegerField(default=3)
    marital_status = models.CharField(max_length=20, blank=True, default='')
    number_of_address = models.IntegerField(default=1)
    complain = models.IntegerField(default=0)
    order_amount_hike_from_last_year = models.IntegerField(default=0)
    coupon_used = models.IntegerField(default=0)
    cashback_amount = models.FloatField(default=0.0)

    # ----------------------------
    # Prediction results
    # ----------------------------
    churn_prediction = models.IntegerField(null=True, blank=True)
    churn_probability = models.FloatField(null=True, blank=True)
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, null=True, blank=True)

    # ----------------------------
    # Metadata and ownership
    # ----------------------------
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Function: __str__
    def __str__(self):
        return f"{self.name} ({self.email})"

# Class: Meta
    class Meta:
        ordering = ['-created_at']
