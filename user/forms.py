from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Guestbook

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname=forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username','nickname','id', 'email','phone_number', 'password1', 'password2']

class LoginForm(forms.Form):
    id=forms.CharField(label='아이디')
    password=forms.CharField(label='비밀번호', widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta :
        model = CustomUser
        fields = ['nickname', 'id', 'password']

class GuestbookForm(forms.ModelForm):
    message = forms.CharField(max_length=100, widget=forms.Textarea(attrs={
        'placeholder': '방명록을 남겨보세요.',
        'rows': 3
    }))

    class Meta:
        model = Guestbook
        fields = ['message']
