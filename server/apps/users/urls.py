from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('login_info/', login_info, name="login_info"),
    path('redirect_view/', redirect_view, name="redirect_view"),
    path("start/",start,name="start"), #시작페이지-추가
     path("nickname_profile_input/",nickname_profile_input,name="nickname_profile_input"), #프로필 사진 닉네임 입력하는 뷰
    
    #채연추가뷰
    path("mypage_list/",mypage_list,name="mypage_list"),
    path("mypage_profile_settings/",mypage_profile_settings,name="mypage_profile_settings"),
    path("start/",start,name="start"),
    path("payment_guide/",payment_guide,name="payment_guide"),
    path("nickname_profile_input/",nickname_profile_input,name="nickname_profile_input"),
   
]
