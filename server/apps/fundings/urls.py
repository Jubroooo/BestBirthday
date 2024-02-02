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
    path('all_birthday_list/',all_birthday_list, name="all_birthday_list"),
    path('all_funding_list/',all_funding_list, name="all_funding_list"),
    path('create_payment/',create_payment, name="create_payment"),
    path('create_funding/',create_funding, name="create_funding"),
    #뷰 확인용
     path('detail/', detail, name="detail"),
]
