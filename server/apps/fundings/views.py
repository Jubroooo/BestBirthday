from django.shortcuts import render, redirect
from .forms import FundingForm, MessageForm
from .models import Funding, Funding_Msg
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.template.defaulttags import register
from django.db.models.functions import Random
import copy
from django.db.models.functions import Length

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
    funding = Funding.objects.all()
    ctx = {"fundings" : funding}
    return render(request, 'fundings/main2.html', ctx)

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
#채연 뷰 확인용--------------------------------------------
def detail(request) :
    return render(request, 'fundings/fundings_detail.html')
def my_detail(request) :
    return render(request, 'fundings/fundings_my_detail.html')

#기존꺼
# def detail(request, pk) :
#     funding = Funding.objects.get(id=pk)
#     progress = int(funding.total_price / funding.goal_price * 100)
#     ctx = {'funding':funding, 'progress':progress}    
#     return render(request, 'fundings/fundings_detail.html', ctx)
def result_modal(request):
    return render(request,'fundings/result_modal.html')
def result_start(request):
    return render(request,'fundings/result_start.html')
def result_list(request):
    return render(request,'fundings/result_list.html')
def result_detail(request):
    return render(request,'fundings/result_detail.html')
def gift_complete(request):
    return render(request,'fundings/gift_complete.html')
def create_payment(request):
    return render(request,'fundings/create_payment.html')
def create_gift(request):
    return render(request,'fundings/create_gift.html')

def create_funding(request) :
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
    progress = int(funding.total_price / funding.goal_price * 100)
    dday = birthday_dday_cal(funding)
    ctx = {'funding':funding, 'progress':progress, "dday":dday}    

    return render(request, 'fundings/fundings_detail.html', ctx)

def create_gift(request, pk) :
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
def create_payment(request):
    return render(request, 'fundings/create_payment.html')

def create_gift_complete(request):
    pass
def create_gift_modal(request):
    pass
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

def main_all_birthday_list(request):
    fundings = Funding.objects.filter(is_closed=False)
    if fundings.exists():
        today = date.today()
        fundings = fundings.filter (user__birthday__month = today.month, user__birthday__day = today.day) 
        funding_dday_dict = funding_dday_cal(fundings)
        ctx = {
            "fundings": fundings,
            "funding_dday_dict": funding_dday_dict,
        }
    
        return render (request, 'fundings/main_all_birthday_list.html', ctx)
    return render (request, 'fundings/main_all_birthday_list.html')

def main_ranking_list(request):
    fundings = Funding.objects.filter(is_closed=False)
    if fundings.exists():
        fundings = fundings.order_by('-msg_count')
        funding_dday_dict = funding_dday_cal(fundings)
        ctx = {
            "fundings": fundings,
            "funding_dday_dict": funding_dday_dict,
        }
    
        return render (request, 'fundings/main_ranking_list.html', ctx)
    return render (request, 'fundings/main_ranking_list.html')

def main_all_funding_list(request):
    fundings = Funding.objects.filter(is_closed=False)
    if fundings.exists():
        fundings = fundings.order_by(Random())
        funding_dday_dict = funding_dday_cal(fundings)
        ctx = {
            "fundings": fundings,
            "funding_dday_dict": funding_dday_dict,
        }
    
        return render (request, 'fundings/main_all_funding_list.html', ctx)
    return render (request, 'fundings/main_all_funding_list.html')


def result_start(request, pk):
    funding_msgs = Funding_Msg.objects.filter(post_id=pk)
    print (funding_msgs)
    if funding_msgs.exists():
        earliest_msg = funding_msgs.earliest('written_date')
        longest_msg = funding_msgs.annotate(content_length=Length('content')).order_by('-content_length').first()
        ctx = {
            'pk': pk,
            'earliest_msg': earliest_msg,
            'longest_msg': longest_msg,
        }
        return render (request, 'fundings/fundings_view_messages.html', ctx)
    else:
        return render (request, 'fundings/fundings_view_messages.html')


def result_list(request, pk):
    funding_msgs = Funding_Msg.objects.filter(post_id = pk)
    funding_msg_count = funding_msgs.count()
    ctx = {
        "funding_msg_count": funding_msg_count,
        "funding_msgs": funding_msgs,
    }
    
    return render (request, 'fundings/fundings_view_all_messages.html', ctx)

def result_detail (request, pk):
    funding_msg = Funding_Msg.objects.get(id=pk)
    ctx = {
        "funding_msg": funding_msg,
    }
    
    return render (request, "fundings/funding_msg_detail.html", ctx)