from django.shortcuts import render, redirect
from .forms import *
from .models import Funding, Funding_Msg
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.template.defaulttags import register
from django.db.models.functions import Length
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser


#딕셔너리 필터링 함수
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

#0. 시작하기
def start(request):
    return render(request,'fundings/start.html')

#1-1 펀딩 확인 뷰
def main(request) :
    #열려 있는 펀딩들 랜덤으로 정렬
    open_fundings = Funding.objects.filter(is_closed=False)
        
    if open_fundings.exists():
        today = date.today()
        today_fundings = open_fundings.filter(user__birthday__month = today.month, user__birthday__day = today.day) 
        today_fundings_num=today_fundings.count()
        total_today_funding_msg_count = 0

        # 오늘 생일 펀딩 메시지 세기
        for funding in today_fundings:
            msg_count = Funding_Msg.objects.filter(post=funding).count()
            total_today_funding_msg_count += msg_count

        today_fundings = today_fundings[:3]
        fundings_in_msg_order = open_fundings.order_by('-msg_count')
        fundings_in_msg_order = fundings_in_msg_order[:3]
        
        open_fundings = open_fundings[:3]
        
        today_funding_dday_dict = funding_dday_cal(today_fundings)
        msg_funding_dday_dict = funding_dday_cal(fundings_in_msg_order)
        open_funding_dday_dict = funding_dday_cal(open_fundings)
        today_funding_progress_dict = funding_progress(today_fundings)
        msg_funding_progress_dict = funding_progress(fundings_in_msg_order)
        open_funding_progress_dict = funding_progress(open_fundings)
        funding_exists = funding_exist_check(request)
        ctx = {"today_fundings":today_fundings, 
               "today_fundings_num":today_fundings_num,
               "total_today_funding_msg_count":total_today_funding_msg_count,
            "today_funding_dday_dict":today_funding_dday_dict,
            "fundings_in_msg_order":fundings_in_msg_order,
            "msg_funding_dday_dict":msg_funding_dday_dict,
            "open_fundings":open_fundings,
            "open_funding_dday_dict":open_funding_dday_dict,
            "today_funding_progress_dict":today_funding_progress_dict,
            "msg_funding_progress_dict":msg_funding_progress_dict,
            "open_funding_progress_dict":open_funding_progress_dict,
            'funding_exists': funding_exists, # 1유저 1펀딩 위한 
            }
        return render(request, 'fundings/main.html', ctx)
    else:
        return render(request, 'fundings/main.html')

def main_all_birthday_list(request):
    fundings = Funding.objects.filter(is_closed=False)
    if fundings.exists():
        today = date.today()
        fundings = fundings.filter (user__birthday__month = today.month, user__birthday__day = today.day) 
        funding_dday_dict = funding_dday_cal(fundings)
        funding_progresses = funding_progress(fundings)
        ctx = {
            "fundings": fundings,
            "funding_dday_dict": funding_dday_dict,
            "funding_progresses": funding_progresses,
        }
    
        return render (request, 'fundings/main_all_birthday_list.html', ctx)
    return render (request, 'fundings/main_all_birthday_list.html')

def main_ranking_list(request):
    fundings = Funding.objects.filter(is_closed=False)
    if fundings.exists():
        fundings = fundings.order_by('-msg_count')
        funding_dday_dict = funding_dday_cal(fundings)
        funding_progresses = funding_progress(fundings)
        ctx = {
            "fundings": fundings,
            "funding_dday_dict": funding_dday_dict,
            "funding_progresses": funding_progresses
        }
    
        return render (request, 'fundings/main_ranking_list.html', ctx)
    return render (request, 'fundings/main_ranking_list.html')

def main_all_funding_list(request):
    fundings = Funding.objects.filter(is_closed=False)
    if fundings.exists():
        funding_dday_dict = funding_dday_cal(fundings)
        funding_progresses = funding_progress(fundings)
        ctx = {
            "fundings": fundings,
            "funding_dday_dict": funding_dday_dict,
            "funding_progresses": funding_progresses
        }
    
        return render (request, 'fundings/main_all_funding_list.html', ctx)
    return render (request, 'fundings/main_all_funding_list.html')

def detail(request, pk) :
    funding = Funding.objects.get(id=pk)
    progress = int(funding.total_price / funding.goal_price * 100)
    dday = birthday_dday_cal(funding)
    ctx = {'funding':funding, 'progress':progress, "dday":dday}   
    return render(request, 'fundings/detail.html', ctx)

#1-2 펀딩 참여 뷰
def create_gift(request, pk):
    funding = Funding.objects.get(id = pk)
    if request.user.is_authenticated:
        if request.method == "GET":
            funding_msg = Funding_Msg()
            funding_msg.user = request.user
            funding_msg.post = funding
            form = MessageForm(instance=funding_msg)
            ctx = {
                'form':form, 'funding':funding
            }
            return render(request, 'fundings/create_gift.html', ctx)
        
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
                return redirect('fundings:create_gift_complete',pk)
            else:
                ctx = {
                    "form":form, 'funding':funding
                }
                return render (request, 'fundings/create_gift.html', ctx)
    
    else:
        if request.method == "GET":
            funding_msg = Funding_Msg()
            funding_msg.post = funding
            form = MessageForm(instance=funding_msg)
            ctx = {
                'form':form, 'funding':funding
            }
            return render(request, 'fundings/create_gift.html', ctx)
        
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
                return redirect('fundings:create_gift_complete',pk)
            else:
                ctx = {
                    "form":form, 'funding':funding
                }
                return render(request, 'fundings/create_gift.html', ctx)

def create_gift_complete(request,pk):
    funding = Funding.objects.get(id = pk)
    ctx = {
        'funding': funding,
        'pk': pk
    }
    return render(request, 'fundings/gift_complete.html',ctx)

#2. 펀딩 생성 관련 뷰
def create_funding(request) :
    if request.user.is_authenticated:
        if request.method == 'GET':
             #유저의 계좌가 없을때 계좌페이지로 이동
            if request.user.toss_account is None and request.user.kakao_account is None:
                return render(request, 'fundings/create_payment.html')

            # 계좌가 있는 경우 펀딩 생성 폼을 보여줌
            funding = Funding(user=request.user)
            form = FundingForm(instance=funding)
            return render(request, 'fundings/create_funding.html', {'form': form})
        
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
                return render (request, 'fundings/create_funding.html', ctx)
    else:
        return redirect('users:login')
    

def create_payment(request):
    user=request.user
    #추가
    from_page = request.GET.get('from', '')
    if from_page == 'list':
        ctx = {"user":user,
               'from_page': from_page
               }
        return render(request, 'fundings/create_payment.html', ctx)
    ctx={"user":user}
    return render(request, 'fundings/create_payment.html', ctx)


#3. 결과 관련 뷰
def result_modal(request, pk):
    funding = Funding.objects.get(id = pk)
    ctx = {
        'funding': funding,
    }
    return render(request,'fundings/result_modal.html', ctx)

def result_start(request, pk):
    funding = Funding.objects.get(id = pk)
    funding_msgs = Funding_Msg.objects.filter(post_id=pk)
    funding_msg_count = funding_msgs.count() 
    if funding_msgs.exists():
        earliest_msg = funding_msgs.earliest('written_date')
        longest_msg = funding_msgs.annotate(content_length=Length('content')).order_by('-content_length').first()
        ctx = {
            'funding':funding,
            'pk': pk,
            "funding_msgs": funding_msgs,
            'earliest_msg': earliest_msg,
            'longest_msg': longest_msg,
            'funding_msg_count': funding_msg_count,  # funding_msg_count 변수 추가
        }
        return render (request, 'fundings/result_start.html', ctx)
    else:
         ctx = {
            'funding':funding,
            'pk': pk,
            'funding_msg_count': funding_msg_count,  # funding_msg_count 변수 추가
        }
         return render (request, 'fundings/result_start.html',ctx)

def result_detail (request, pk):
    funding_msg = Funding_Msg.objects.get(id=pk)
    ctx = {
        "funding_msg": funding_msg,
    }
    return render (request, "fundings/result_detail.html", ctx)
    
# 기타: 함수들
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

#펀딩 진행률 함수
def funding_progress(fundings):
    funding_progress_dict = {} #펀딩 진행 딕셔너리

    for funding in fundings:
        funding_progress_dict[funding.id] = int(funding.total_price / funding.goal_price * 100)

    return funding_progress_dict

def finish(request, pk):
    if request.method == "POST":
        funding = Funding.objects.get(id=pk)
        funding.is_closed = True
        funding.save()
        return redirect ('fundings:result_modal', pk=pk)
    
#1인 1펀딩을 위한 열려있는 펀딩 체크 확인 함수    
def funding_exist_check(request):
    #에러코드0 == 로그인한 유저가 아닐때
    if request.user.is_anonymous:
           return 0 
    #생일 기한 인지 확인하는 부분
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    birthday_month, birthday_day = request.user.birthday.month, request.user.birthday.day
    current_year_birthday = datetime(current_date.year, birthday_month, birthday_day)
    if current_date > current_year_birthday:
        day_difference = current_date - current_year_birthday
    else:
        day_difference = current_year_birthday - current_date
    if day_difference.days > 7:
        return 1
    #에러코드1 == 생일 기한 아님
    
    current_time = timezone.now()
    temp_fundings = Funding.objects.filter(user=request.user)
    temp_fundings = temp_fundings.filter(created_date__gte=current_time-timezone.timedelta(days=7))
    temp_fundings = temp_fundings.filter(is_closed=False)
    funding_exists = temp_fundings.exists()

    # 에러코드2 == 펀딩메세지 존재 
    if funding_exists:
        return 2
