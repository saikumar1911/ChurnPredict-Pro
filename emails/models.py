from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer

class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('sent', '✅ Sent'),
        ('delivered', '📬 Delivered'),
        ('opened', '👁️ Opened'),
        ('failed', '❌ Failed'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='emails')
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500)
    message = models.TextField()
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    discount_percent = models.IntegerField(default=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Email to {self.customer.name} on {self.sent_at}"
    
    class Meta:
        ordering = ['-sent_at']