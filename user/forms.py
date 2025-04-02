from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname=forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username','nickname', 'email','phone_number', 'password1', 'password2']