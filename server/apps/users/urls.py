from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    #채연추가뷰
    path("birth_input/",birth_input,name="birth_input"),
    path("mypage_list/",mypage_list,name="mypage_list"),
    path("mypage_profile_settings/",mypage_profile_settings,name="mypage_profile_settings"),
    path("start/",start,name="start"),
    path("payment_guide/",payment_guide,name="payment_guide"),
    path("nickname_profile_input/",nickname_profile_input,name="nickname_profile_input"),
   
]
