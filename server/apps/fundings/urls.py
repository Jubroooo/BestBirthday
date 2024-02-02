from django.urls import path
from .views import *

app_name = 'fundings'

urlpatterns = [
    path('', main, name="main"),
    path('create/', create, name="create"),
    # path('detail/<int:pk>/', detail, name="detail"), 
    path('delete/<int:pk>/', delete, name="delete"), 
    path('update/<int:pk>/', update, name="update"),
    path('message/create', message, name="message"),
    # 예진 추가뷰
    path('all_birthday_list/',all_list),
    #뷰 확인용
     path('detail/', detail, name="detail"),
]
