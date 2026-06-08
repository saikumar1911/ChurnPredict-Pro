# File: accounts/forms.py



# Import section
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Login form for store managers.
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 10px; font-size: 14px;',
                'autocomplete': 'username',
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 10px; font-size: 14px;',
                'autocomplete': 'current-password',
            }
        )
    )

# Registration form for new store managers.
class RegisterForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'style': 'flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px;',
            }
        )
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'style': 'flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px;',
            }
        )
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username *',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px;',
                'autocomplete': 'username',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email *',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px;',
                'autocomplete': 'email',
            }
        )
    )
    store_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Store Name (optional)',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px;',
            }
        )
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Phone (optional)',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px;',
                'autocomplete': 'tel',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password *',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px;',
                'autocomplete': 'new-password',
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password *',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px;',
                'autocomplete': 'new-password',
            }
        )
    )

# Function: clean_username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # If block
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists!')
        return username

# Function: clean_email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # If block
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered!')
        return email

# Function: clean
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # If block
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match!')

        return cleaned_data
