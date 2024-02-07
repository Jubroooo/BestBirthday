from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('login_info/', login_info, name="login_info"),
    path('redirect_view/', redirect_view, name="redirect_view"),
    path("nickname_profile_input/",nickname_profile_input,name="nickname_profile_input"),
    #마이페이지 관련
    path('mypage_list/', mypage_list, name="mypage_list"), 
    path('mypage_profile_setting/', mypage_profile_setting, name="mypage_profile_setting"), 
    path('mypage_payment_guide_k/', mypage_payment_guide_k, name="mypage_payment_guide_k"), 
    path('mypage_payment_guide_t/', mypage_payment_guide_t, name="mypage_payment_guide_t"), 
    path('mypage_myfunding/', mypage_myfunding, name="mypage_myfunding"), 
    path('mypage_participated/', mypage_participated, name="mypage_participated"),
]
