from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    #채연추가뷰
    path("birth_input/",birth_input,name="birth_input"),
    #예진추가뷰
    path("mypage_myfunding/",mypage_myfunding,name="mypage_myfunding"),
    path("mypage_participated/",mypage_participated,name="mypage_participated"),
]
