from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname=forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username','nickname','id', 'email','phone_number', 'password1', 'password2']



class LoginForm(forms.Form):
    id=forms.CharField(label='아이디')
    password=forms.CharField(label='비밀번호', widget=forms.PasswordInput)