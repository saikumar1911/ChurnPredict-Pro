# File: emails/views.py



# Import section
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import string
from customers.models import Customer
from .models import EmailLog

# Helper to create a unique coupon code for the email.
def generate_coupon(customer_name, discount):
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
    number = random.randint(100, 999)
    return f"{prefix}{discount}{number}"

@login_required
# Function: email_list
def email_list(request):
    """Show the list of emails sent by the current user."""
    emails = EmailLog.objects.filter(sent_by=request.user).select_related('customer')
    context = {
        'emails': emails,
        'total': emails.count(),
    }
    return render(request, 'emails/list.html', context)

@login_required
# Function: send_email
def send_email(request, customer_id):
    """Compose and save a retention email for a customer."""
    customer = get_object_or_404(Customer, id=customer_id, created_by=request.user)

    # If block
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        discount = int(request.POST.get('discount', 20))

        coupon = generate_coupon(customer.name, discount)

        EmailLog.objects.create(
            customer=customer,
            sent_by=request.user,
            subject=subject,
            message=message,
            coupon_code=coupon,
            discount_percent=discount,
            status='sent'
        )

        profile = request.user.profile
        profile.total_emails_sent += 1
        profile.save()

        messages.success(request, f'Email sent to {customer.name}! Coupon: {coupon}')
        return redirect('customers:customer_detail', customer_id=customer.id)

    # Default discount based on churn risk.
    # If block
    if customer.risk_level == 'High':
        default_discount = 25
    # Elif block
    elif customer.risk_level == 'Medium':
        default_discount = 15
    # Else block
    else:
        default_discount = 10

    return render(request, 'emails/send.html', {
        'customer': customer,
        'default_discount': default_discount
    })
