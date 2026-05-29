from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from customers.models import Customer
from .models import EmailLog

def generate_coupon(customer_name, discount):
    """Generate unique coupon code"""
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
    number = random.randint(100, 999)
    return f"{prefix}{discount}{number}"

@login_required
def email_list(request):
    emails = EmailLog.objects.filter(sent_by=request.user).select_related('customer')
    
    context = {
        'emails': emails,
        'total': emails.count(),
    }
    return render(request, 'emails/list.html', context)

@login_required
def send_email(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, created_by=request.user)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        discount = int(request.POST.get('discount', 20))
        
        # Generate coupon
        coupon = generate_coupon(customer.name, discount)
        
        # Save to database
        email_log = EmailLog.objects.create(
            customer=customer,
            sent_by=request.user,
            subject=subject,
            message=message,
            coupon_code=coupon,
            discount_percent=discount,
            status='sent'
        )
        
        # Send real email (uncomment in production)
        # send_mail(
        #     subject,
        #     f"{message}\n\nYour coupon: {coupon}\nDiscount: {discount}%",
        #     settings.EMAIL_HOST_USER,
        #     [customer.email],
        #     fail_silently=False,
        # )
        
        # Update manager stats
        profile = request.user.profile
        profile.total_emails_sent += 1
        profile.save()
        
        messages.success(request, f'Email sent to {customer.name}! Coupon: {coupon}')
        return redirect('customers:customer_detail', customer_id=customer.id)
    
    # Default discount based on risk level
    if customer.risk_level == 'High':
        default_discount = 25
    elif customer.risk_level == 'Medium':
        default_discount = 15
    else:
        default_discount = 10
    
    return render(request, 'emails/send.html', {
        'customer': customer,
        'default_discount': default_discount
    })