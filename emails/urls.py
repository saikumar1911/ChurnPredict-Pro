from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    path('', views.email_list, name='email_list'),
    path('send/<int:customer_id>/', views.send_email, name='send_email'),
]