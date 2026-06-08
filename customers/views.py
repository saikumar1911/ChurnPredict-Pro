# File: customers/views.py



# Import section
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import pandas as pd
from .models import Customer

@login_required
# Function: customer_list
def customer_list(request):
    """Display the current user's customers with search and filter support."""
    customers = Customer.objects.filter(created_by=request.user)

    risk_filter = request.GET.get('risk')
    # If block
    if risk_filter:
        customers = customers.filter(risk_level=risk_filter)

    search = request.GET.get('search')
    # If block
    if search:
        customers = customers.filter(
            Q(name__icontains=search) | Q(email__icontains=search)
        )

    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    stats = Customer.objects.filter(created_by=request.user)
    context = {
        'customers': page_obj,
        'total': stats.count(),
        'high_risk': stats.filter(risk_level='High').count(),
        'medium_risk': stats.filter(risk_level='Medium').count(),
        'low_risk': stats.filter(risk_level='Low').count(),
    }
    return render(request, 'customers/list.html', context)

@login_required
# Function: add_customer
def add_customer(request):
    """Create a new customer record from the add form."""
    # If block
    if request.method == 'POST':
        customer = Customer(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone', ''),
            total_orders=int(request.POST.get('total_orders', 0)),
            total_spent=float(request.POST.get('total_spent', 0)),
            days_since_last_order=int(request.POST.get('days_since_last_order', 0)),
            complaint_count=int(request.POST.get('complaint_count', 0)),
            tenure=int(request.POST.get('tenure', 0)),
            created_by=request.user
        )
        customer.save()
        messages.success(request, f'Customer {customer.name} added!')
        return redirect('customers:customer_list')

    return render(request, 'customers/add.html')

@login_required
# Function: edit_customer
def edit_customer(request, customer_id):
    """Update an existing customer record."""
    customer = get_object_or_404(Customer, id=customer_id, created_by=request.user)

    # If block
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone', '')
        customer.total_orders = int(request.POST.get('total_orders', 0))
        customer.total_spent = float(request.POST.get('total_spent', 0))
        customer.days_since_last_order = int(request.POST.get('days_since_last_order', 0))
        customer.complaint_count = int(request.POST.get('complaint_count', 0))
        customer.tenure = int(request.POST.get('tenure', 0))
        customer.save()
        messages.success(request, f'Customer {customer.name} updated!')
        return redirect('customers:customer_list')

    return render(request, 'customers/edit.html', {'customer': customer})

@login_required
# Function: delete_customer
def delete_customer(request, customer_id):
    """Delete a customer record and show a success message."""
    customer = get_object_or_404(Customer, id=customer_id, created_by=request.user)
    name = customer.name
    customer.delete()
    messages.success(request, f'Customer {name} deleted!')
    return redirect('customers:customer_list')

@login_required
# Function: customer_detail
def customer_detail(request, customer_id):
    """Display the details for a single customer."""
    customer = get_object_or_404(Customer, id=customer_id, created_by=request.user)
    return render(request, 'customers/detail.html', {'customer': customer})

@login_required
# Function: upload_csv
def upload_csv(request):
    """Upload a CSV file and import customer rows."""
    # If block
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # If block
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file!')
            return redirect('customers:customer_list')

        # Try block
        try:
            df = pd.read_csv(csv_file)
            success_count = 0
            error_count = 0

            # For block
            for _, row in df.iterrows():
                name = row.get('name', row.get('Name', ''))
                email = row.get('email', row.get('Email', ''))
                # If block
                if not name or not email:
                    error_count += 1
                    continue

                # Try block
                try:
                    Customer.objects.create(
                        name=str(name),
                        email=str(email),
                        phone=str(row.get('phone', row.get('Phone', ''))),
                        total_orders=int(row.get('total_orders', row.get('orders', 0))),
                        total_spent=float(row.get('total_spent', row.get('spent', 0))),
                        days_since_last_order=int(row.get('days_since_last_order', row.get('days', 0))),
                        complaint_count=int(row.get('complaint_count', row.get('complaints', 0))),
                        tenure=int(row.get('tenure', row.get('Tenure', 0))),
                        city_tier=int(row.get('city_tier', row.get('City Tier', 1))),
                        created_by=request.user
                    )
                    success_count += 1
                # Except block
                except Exception:
                    error_count += 1

            messages.success(request, f'Uploaded {success_count} customers successfully! Errors: {error_count}')
            return redirect('customers:customer_list')
        # Except block
        except Exception as exc:
            messages.error(request, f'Error reading CSV: {exc}')
            return redirect('customers:customer_list')

    return render(request, 'customers/upload.html')
