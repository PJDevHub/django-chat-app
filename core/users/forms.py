from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)

    consent = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
            'email',
            'phone',
            'password1',
            'password2'
        )