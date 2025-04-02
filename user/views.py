from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from user.forms import SignUpForm
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.contrib.auth.hashers import make_password

@login_required
def home(request):
    print(f"현재 로그인한 사용자: {request.user.username}")
    return render(request, "home.html", {'username':request.user.username})

def signup_view(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/user/accounts/login/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form':form})

def PasswordResetView(request):
    return render(request, "registration/password_reset.html", {})

def password_reset(request):
    if request.method == "POST":
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if new_password1 and new_password1 == new_password2:
            user = request.user
            user.password = make_password(new_password1)
            user.save()
            return redirect('/user/accounts/login/')
        else:
            error_message = "비밀번호가 일치하지 않습니다."
            return render(request, "registration/password_reset.html", {"error_message": error_message})

    return render(request, "registration/password_reset.html")

def password_change(request):
    return render(request, "registration/password_change.html", {})
 
def send_email(request):
    subject = "message"
    to = ["justfortestqwe@gmail.com"]
    from_email = "id@gmail.com"
    message = "메세지 테스트"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()