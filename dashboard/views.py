# File: dashboard/views.py



# Import section
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from emails.models import EmailLog

@login_required
# Function: dashboard_view
def dashboard_view(request):
    """Render the dashboard with summary statistics and recent customers."""
    customers = Customer.objects.filter(created_by=request.user)

    total = customers.count()
    high = customers.filter(risk_level='High').count()
    medium = customers.filter(risk_level='Medium').count()
    low = customers.filter(risk_level='Low').count()
    pending = customers.filter(risk_level__isnull=True).count()

    emails_sent = EmailLog.objects.filter(sent_by=request.user).count()
    recent_customers = customers.order_by('-created_at')[:5]
    high_percent = round((high / total * 100), 1) if total else 0

    context = {
        'total': total,
        'high': high,
        'medium': medium,
        'low': low,
        'pending': pending,
        'high_percent': high_percent,
        'emails_sent': emails_sent,
        'recent_customers': recent_customers,
    }
    return render(request, 'dashboard/index.html', context)
