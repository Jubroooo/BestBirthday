from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
<<<<<<< HEAD
=======
    path('login_info/', login_info, name="login_info"),
    path('redirect_view/', redirect_view, name="redirect_view"),
>>>>>>> 98a6ae70da005bc85356552c1007c1b9e74e7cdf
]
