from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('login_info/', login_info, name="login_info"),
    path('redirect_view/', redirect_view, name="redirect_view"),
]
