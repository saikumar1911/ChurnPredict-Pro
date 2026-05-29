from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import pandas as pd
from .models import Customer

@login_required
def customer_list(request):
    customers = Customer.objects.filter(created_by=request.user)
    
    # Filter by risk level
    risk_filter = request.GET.get('risk')
    if risk_filter:
        customers = customers.filter(risk_level=risk_filter)
    
    # Search
    search = request.GET.get('search')
    if search:
        customers = customers.filter(name__icontains=search) | customers.filter(email__icontains=search)
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customers': page_obj,
        'total': Customer.objects.filter(created_by=request.user).count(),
        'high_risk': Customer.objects.filter(created_by=request.user, risk_level='High').count(),
        'medium_risk': Customer.objects.filter(created_by=request.user, risk_level='Medium').count(),
        'low_risk': Customer.objects.filter(created_by=request.user, risk_level='Low').count(),
    }
    return render(request, 'customers/list.html', context)

@login_required
def add_customer(request):
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
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, created_by=request.user)
    
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
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, created_by=request.user)
    name = customer.name
    customer.delete()
    messages.success(request, f'Customer {name} deleted!')
    return redirect('customers:customer_list')

@login_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, created_by=request.user)
    return render(request, 'customers/detail.html', {'customer': customer})

@login_required
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file!')
            return redirect('customers:customer_list')
        
        try:
            df = pd.read_csv(csv_file)
            success_count = 0
            error_count = 0
            
            for index, row in df.iterrows():
                try:
                    name = row.get('name', row.get('Name', ''))
                    email = row.get('email', row.get('Email', ''))
                    
                    if name and email:
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
                    else:
                        error_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Error on row {index}: {e}")
            
            messages.success(request, f'Uploaded {success_count} customers successfully! Errors: {error_count}')
            return redirect('customers:customer_list')
            
        except Exception as e:
            messages.error(request, f'Error reading CSV: {str(e)}')
            return redirect('customers:customer_list')
    
    return render(request, 'customers/upload.html')