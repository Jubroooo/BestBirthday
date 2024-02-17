from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth import logout as account_logout
from ..fundings.models import *
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.urls import reverse
        
def login(request):
    return render (request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect ('fundings:main')

def delete_user(request):
    request.user.delete()
    account_logout(request)
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


# 마이페이지 뷰
def mypage_list(request):
    user=request.user
    ctx={"user":user}
    return render(request,'users/mypage_list.html',ctx)

def mypage_myfunding(request):
    user = request.user
    myfundings = user.funding_user.all()
    funding_dday_dict = funding_dday_cal(myfundings)
    funding_progress_dict = funding_progress(myfundings)
    ctx={
        "myfundings":myfundings,
        "funding_dday_dict":funding_dday_dict,
        "funding_progress_dict":funding_progress_dict        
    }
    return render(request,"users/mypage_myfunding.html", ctx)

def mypage_participated(request):
    current_user = request.user
    # 유저가 쓴 메세지 필터링
    fundings_participated_in = Funding_Msg.objects.filter(user=current_user).values_list('post', flat=True)

    # 메세지ID가 포함된 펀딩글 필터링
    participated_fundings = Funding.objects.filter(id__in=fundings_participated_in)
    funding_dday_dict = funding_dday_cal(participated_fundings)
    funding_progress_dict = funding_progress(participated_fundings)
    ctx={
        "participated_fundings":participated_fundings,
        "funding_dday_dict":funding_dday_dict,
        "funding_progress_dict":funding_progress_dict        
    }
    
    return render(request, "users/mypage_participated.html", ctx)

def mypage_profile_setting(request):
    user = request.user
    if request.method == "POST":
        form = UserProfilesettingForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect ('users:mypage_list')
    else:
        form = UserProfilesettingForm(instance=user)
    ctx = {
        "form": form,
    }
    return render(request,'users/mypage_profile_setting.html', ctx)    


def mypage_payment_guide_k(request):
    user = request.user
    from_list = request.GET.get('from', None) 
    if request.method == "POST":
        form = kakaoForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            if from_list:
                # 'fundings:create_payment' 패턴 이름을 사용하여 URL 가져오기
                create_payment_url = reverse('fundings:create_payment') + '?from=' + from_list
                return redirect(create_payment_url)
            else:
                return redirect('fundings:create_payment')
    else:
        form = kakaoForm(instance=user)
    ctx = {
        "form": form,
    }        
    return render(request,'users/mypage_payment_guide_k.html', ctx)

def mypage_payment_guide_t(request):
    user = request.user
    from_list = request.GET.get('from', None)
    if request.method == "POST":
        form = tossForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            if from_list:
                # 'fundings:create_payment' 패턴 이름을 사용하여 URL 가져오기
                create_payment_url = reverse('fundings:create_payment') + '?from=' + from_list
                return redirect(create_payment_url)
            else:
                return redirect('fundings:create_payment')
    else:
        form = tossForm(instance=user)
    ctx = {
        "form": form,
    }
    return render(request,'users/mypage_payment_guide_t.html', ctx)

#펀딩 날짜 계산
def funding_dday_cal(fundings):
     
    funding_dday_dict = {} #펀딩 디데이 딕셔너리

    for funding in fundings:
        current_date = timezone.now()
 
        #펀딩 디데이 계산
        funding_dday = (funding.created_date + timedelta(days=7)) - current_date
        if funding_dday < timedelta(0):
            funding.is_closed = True
        
        funding_dday_dict[funding.id] = funding_dday.days
    return funding_dday_dict

#펀딩 진행률 함수
def funding_progress(fundings):
    funding_progress_dict = {} #펀딩 진행 딕셔너리

    for funding in fundings:
        funding_progress_dict[funding.id] = int(funding.total_price / funding.goal_price * 100)

    return funding_progress_dict