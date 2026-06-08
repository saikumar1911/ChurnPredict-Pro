# File: predictions/urls.py



# Import section
from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('run/', views.run_bulk_prediction, name='run_bulk'),
    path('single/<int:customer_id>/', views.predict_single, name='predict_single'),
]
