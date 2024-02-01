from django.shortcuts import render, redirect
from .forms import FundingForm, MessageForm
from .models import Funding, Funding_Msg
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.template.defaulttags import register
from django.db.models.functions import Random
import copy

#딕셔너리 필터링 함수
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def main(request) :
    #열려 있는 펀딩들 랜덤으로 정렬
    open_fundings = Funding.objects.filter(is_closed=False).order_by(Random())
    if open_fundings.exists():
        today = date.today()
        today_fundings = open_fundings.filter (user__birthday__month = today.month, user__birthday__day = today.day) 
        today_fundings = today_fundings[:3]
        
        fundings_in_msg_order = open_fundings.order_by('-msg_count')
        fundings_in_msg_order = fundings_in_msg_order[:3]
        
        open_fundings = open_fundings[:3]
        
        today_funding_dday_dict = funding_dday_cal(today_fundings)
        msg_funding_dday_dict = funding_dday_cal(fundings_in_msg_order)
        open_funding_dday_dict = funding_dday_cal(open_fundings)
    
            

        ctx = {"today_fundings": today_fundings, 
            "today_funding_dday_dict": today_funding_dday_dict,
            "fundings_in_msg_order": fundings_in_msg_order,
            "msg_funding_dday_dict": msg_funding_dday_dict,
            "open_fundings": open_fundings,
            "open_funding_dday_dict": open_funding_dday_dict
            }
        return render(request, 'fundings/main.html', ctx)
    else:
        return render(request, 'fundings/main.html')

def create(request) :
    if request.user.is_authenticated:
        if request.method == 'GET':
            funding = Funding()
            funding.user = request.user
            form = FundingForm(instance=funding)
            ctx = {
                'form':form
            }
            return render(request, 'fundings/fundings_create.html', ctx)
        #post일때
        elif request.method == "POST":
            funding = Funding()
            funding.user = request.user
            form = FundingForm(request.POST, request.FILES, instance=funding)
            if form.is_valid():
                form.save()
                funding_id = funding.id
                return redirect('fundings:main')
            else:
                ctx = {
                    "form": form
                }
                return render (request, 'fundings/fundings_create.html', ctx)
    else:
        return redirect('users:login')
def detail(request, pk) :
    funding = Funding.objects.get(id=pk)
    progress = int((funding.total_price / funding.goal_price) * 100)
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

def create_message(request, pk) :
    funding = Funding.objects.get (id = pk)
    if request.user.is_authenticated:
        if request.method == "GET":
            funding_msg = Funding_Msg()
            funding_msg.user = request.user
            funding_msg.post = funding
            form = MessageForm(instance=funding_msg)
            ctx = {
                'form':form
            }
            return render(request, 'fundings/fundings_message_create.html', ctx)
        
        elif request.method == "POST":
            funding_msg = Funding_Msg()
            funding_msg.user = request.user
            funding_msg.post = funding
            form = MessageForm(request.POST, instance=funding_msg)
            if form.is_valid():
                form.save()
                funding.total_price = funding.total_price + funding_msg.funding_price 
                funding.msg_count += 1
                if funding.total_price >= funding.goal_price:
                    funding.is_achieved = True
                funding.save()
                return redirect('fundings:main')
            else:
                ctx = {
                    "form": form
                }
                return render (request, 'fundings/fundings_message_create.html', ctx)
    
    else:
        if request.method == "GET":
            funding_msg = Funding_Msg()
            funding_msg.post = funding
            form = MessageForm(instance=funding_msg)
            ctx = {
                'form':form
            }
            return render(request, 'fundings/fundings_message_create.html', ctx)
        
        elif request.method == "POST":
            funding_msg = Funding_Msg()
            funding_msg.post = funding
            form = MessageForm(request.POST, instance=funding_msg)
            if form.is_valid():
                form.save()
                funding.total_price = funding.total_price + funding_msg.funding_price 
                funding.msg_count += 1
                if funding.total_price >= funding.goal_price:
                    funding.is_achieved = True
                funding.save()
                return redirect('fundings:main')
            else:
                ctx = {
                    "form": form
                }
                return render (request, 'fundings/fundings_message_create.html', ctx)
def funding_dday_cal(fundings):
     
    funding_dday_dict = {} #펀딩 디데이 딕셔너리

    #생일 디데이 계산, 펀딩 디데이 계산 // 함수화 필요할듯!
    for funding in fundings:
        user = funding.user
        current_date = timezone.now()
 
        #펀딩 디데이 계산
        funding_dday = (funding.created_date + timedelta(days=7)) - current_date
        if funding_dday < timedelta(0):
            funding.is_closed = True
        
        funding_dday_dict[user.id] = funding_dday.days

    return copy.deepcopy(funding_dday_dict)

def birthday_dday_cal(funding):
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

    return dday
    # 생일이 지난 경우 양수, 생일이 다가올때는(생일 전에는) 음수값을 전달한다

def today_funding(request):
    fundings = Funding.objects.filter(is_closed=False)
    if fundings.exists():
        today = date.today()
        fundings = fundings.filter (user__birthday__month = today.month, user__birthday__day = today.day) 
        funding_dday_dict = funding_dday_cal(fundings)
        ctx = {
            "fundings": fundings,
            "funding_dday_dict": funding_dday_dict,
        }
    
        return render (request, 'fundings/fundings_today_funding.html', ctx)
    return render (request, 'fundings/fundings_today_funding.html')

def msg_funding(request):
    fundings = Funding.objects.filter(is_closed=False)
    if fundings.exists():
        fundings = fundings.order_by('-msg_count')
        funding_dday_dict = funding_dday_cal(fundings)
        ctx = {
            "fundings": fundings,
            "funding_dday_dict": funding_dday_dict,
        }
    
        return render (request, 'fundings/fundings_msg_funding.html', ctx)
    return render (request, 'fundings/fundings_msg_funding.html')

def open_funding(request):
    fundings = Funding.objects.filter(is_closed=False)
    if fundings.exists():
        fundings = fundings.order_by(Random())
        funding_dday_dict = funding_dday_cal(fundings)
        ctx = {
            "fundings": fundings,
            "funding_dday_dict": funding_dday_dict,
        }
    
        return render (request, 'fundings/fundings_open_funding.html', ctx)
    return render (request, 'fundings/fundings_open_funding.html')
