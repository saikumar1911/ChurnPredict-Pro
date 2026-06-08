# File: accounts/urls.py



# Import section
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
