from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('add_info/', add_info, name="add_info"),
    path('redirect_view/', redirect_view, name="redirect_view"),
    #path('msg_check/<int:pk>', msg_check, name="msg_check"),
    #채연추가뷰
    path("birth_input/",birth_input,name="birth_input")
]
