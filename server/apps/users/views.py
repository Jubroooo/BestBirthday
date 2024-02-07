from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
        
def login(request):
    return render (request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect ('fundings:main')

def login_info(request): 
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

def nickname_profile_input(request):
    return render(request,'users/nickname_profile_input.html')

def redirect_view(request):
    if request.user.is_authenticated:
        # Check if it's the user's first login
        if request.user.birthday is None or request.user.nickname is None:
            return redirect('users:login_info')  # 소셜 로그인 후 생일 입력하는 화면 
        else:
            return redirect('/')  # Redirect to home for subsequent logins
    else:
        return redirect('/')  # Redirect to home for non-authenticated users


# 4. 마이페이지 뷰(백 작업 필요)
def mypage_list(request):
    return render(request,'users/mypage_list.html')
def mypage_myfunding(request):
    return render(request,"users/mypage_myfunding.html")
def mypage_profile_setting(request):
    return render(request,'users/mypage_profile_setting.html')
def mypage_participated(request):
    return render(request, "users/mypage_participated.html")


def mypage_payment_guide_k(request):
    user = request.user
    if request.method == "POST":
        form = kakaoForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect ('users:mypage_list')
    else:
        form = kakaoForm(instance=user)
    ctx = {
        "form": form,
    }        
    return render(request,'users/mypage_payment_guide_k.html')

def mypage_payment_guide_t(request):
    user = request.user
    if request.method == "POST":
        form = tossForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect ('users:mypage_list')
    else:
        form = tossForm(instance=user)
    ctx = {
        "form": form,
    }        
    return render(request,'users/mypage_payment_guide_t.html')