# File: predictions/views.py



# Import section
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customers.models import Customer
from .ml_model import predict_bulk, predict_single_customer

@login_required
# Function: run_bulk_prediction
def run_bulk_prediction(request):
    """Run churn predictions for all customers owned by the current user."""
    customers = Customer.objects.filter(created_by=request.user)

    # If block
    if not customers.exists():
        messages.warning(request, 'No customers found! Please add customers first.')
        return redirect('customers:customer_list')

    messages.info(request, f'Analyzing {customers.count()} customers...')
    results = predict_bulk(customers)

    # For block
    for result in results:
        customer = Customer.objects.get(id=result['customer_id'])
        customer.churn_prediction = result['prediction']
        customer.churn_probability = result['probability']
        customer.risk_level = result['risk_level']
        customer.save()

    profile = request.user.profile
    profile.total_predictions += 1
    profile.save()

    high_count = sum(1 for r in results if r['risk_level'] == 'High')
    medium_count = sum(1 for r in results if r['risk_level'] == 'Medium')
    low_count = sum(1 for r in results if r['risk_level'] == 'Low')

    messages.success(
        request,
        f'✅ Prediction Complete! High: {high_count}, Medium: {medium_count}, Low: {low_count}'
    )
    return redirect('dashboard:dashboard')

@login_required
# Function: predict_single
def predict_single(request, customer_id):
    """Run prediction for a single customer and save the result."""
    customer = get_object_or_404(Customer, id=customer_id, created_by=request.user)

    customer_dict = {
        'total_orders': customer.total_orders,
        'total_spent': customer.total_spent,
        'days_since_last_order': customer.days_since_last_order,
        'complaint_count': customer.complaint_count,
        'tenure': customer.tenure,
        'city_tier': customer.city_tier,
    }

    prediction, probability = predict_single_customer(customer_dict)

    customer.churn_prediction = prediction
    customer.churn_probability = probability * 100

    # If block
    if probability > 0.7:
        customer.risk_level = 'High'
    # Elif block
    elif probability > 0.4:
        customer.risk_level = 'Medium'
    # Else block
    else:
        customer.risk_level = 'Low'
    customer.save()

    messages.success(
        request,
        f'{customer.name}: {customer.churn_probability:.1f}% churn probability ({customer.risk_level} Risk)'
    )
    return redirect('customers:customer_detail', customer_id=customer.id)
