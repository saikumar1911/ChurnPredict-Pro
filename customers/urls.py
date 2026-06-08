# File: customers/urls.py



# Import section
from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('add/', views.add_customer, name='add_customer'),
    path('edit/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('detail/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('upload/', views.upload_csv, name='upload_csv'),
]
