from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from allauth.account.views import LogoutView
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
#채연추가뷰
# def birth_input(request):
#     return render(request,'users/birth_input.html')
#채연추가뷰--------------------------------------
def login_info(request):
    return render(request,'users/login_info.html')

def nickname_profile_input(request):
    return render(request,'users/nickname_profile_input.html')

#-----------------------------------------------
        
def login(request):
    return render (request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect ('fundings:main')

def login_info(request): #이름, 닉네임, 생일, 프로필 사진 => 카카오에서 받는 건지 
    user = request.user
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect ('fundings:main')
    else:
        form = UserProfileUpdateForm(instance=user)
    ctx = {
        "form": form,
    }        
    return render (request, 'users/login_info.html', ctx)  

def redirect_view(request):
    if request.user.is_authenticated:
        # Check if it's the user's first login
        if request.user.birthday is None or request.user.nickname is None:
            return redirect('users:login_info')  # 소셜 로그인 후 생일 입력하는 화면 
        else:
            return redirect('/')  # Redirect to home for subsequent logins
    else:
        return redirect('/')  # Redirect to home for non-authenticated users

