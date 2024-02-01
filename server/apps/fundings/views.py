from django.shortcuts import render, redirect
from .forms import FundingForm, MessageForm
from .models import Funding, Funding_Msg
from ..users.models import User
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.template.defaulttags import register

#딕셔너리 필터링 함수
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def main(request) :
    fundings = Funding.objects.all()
    dday_dict = {} #생일 디데이 딕셔너리
    funding_dday_dict = {} #펀딩 디데이 딕셔너리

    #생일 디데이 계산, 펀딩 디데이 계산 // 함수화 필요할듯!
    for funding in fundings:
        user = funding.user
        current_date = timezone.now()
        birthday = timezone.make_aware(datetime(current_date.year, user.birthday.month, user.birthday.day), timezone.get_current_timezone()) #time zone으로 설정해야 나중에 배포 시 서버 시간 vs db시간 계산을 할 수 있음
        birthday1 = timezone.make_aware(datetime(current_date.year - 1, user.birthday.month, user.birthday.day), timezone.get_current_timezone())
        dday = (birthday - current_date).days+1

        #생일 지났을 경우
        if dday > -((birthday1 - current_date).days+1): 
            dday = -((birthday1 - current_date).days+1)
        else:
            dday = -dday

        dday_dict[user.id] = dday
        # 생일이 지난 경우 양수, 생일이 다가올때는(생일 전에는) 음수값을 전달한다
        
        #펀딩 디데이 계산
        funding_dday = (funding.created_date + timedelta(days=7)) - current_date
        if funding_dday < timedelta(0):
            funding.is_closed = True
        
        funding_dday_dict[user.id] = funding_dday.days
        

    ctx = {"fundings": fundings, "dday_dict": dday_dict, "funding_dday_dict": funding_dday_dict,}
    return render(request, 'fundings/main.html', ctx)

def create(request) :
    if request.method == 'GET':
        form = FundingForm()
        ctx = {'form':form}
        return render(request, 'fundings/fundings_create.html', ctx)
    #post일때
    form = FundingForm(request.POST, request.FILES)
    if form.is_valid():
        new_funding = form.save(user=request.user)
        pk_of_new_funding = new_funding.pk
        return redirect('fundings:detail', pk=pk_of_new_funding)

def detail(request, pk) :
    funding = Funding.objects.get(id=pk)
    progress = int(funding.total_price / funding.goal_price * 100)
    ctx = {'funding':funding, 'progress':progress}    
    return render(request, 'fundings/fundings_detail.html', ctx)

def delete(request, pk) :
    if request.method == "POST":
        posts = Funding.objects.get(id=pk)
        posts.delete()
        # = Post.objects.get(id=pk).delete()
    return redirect('fundings:main')

def update(request, pk) :
    post=Funding.objects.get(id=pk)
    
    if request.method=='GET':
        form = FundingForm(instance=post)
        ctx = {'form':form, 'pk':pk}
        return render(request, 'fundings/fundings_update.html', ctx)
    
    form=FundingForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()
    return redirect('fundings:detail', pk)

def message(request) :
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, request=request, current_post=current_post)
        if form.is_valid():
            # Save the form
            form.save()
            # Your additional logic here
    else:
        form = MessageForm(request=request, current_post=current_post)