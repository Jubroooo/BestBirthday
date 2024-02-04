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
    # 채연 추가뷰
    path('detail/', detail, name="detail"),
    path('my_detail/', my_detail, name="my_detail"),
    path("result_modal/",result_modal,name="result_modal"),
    path("result_start/",result_start,name="result_start"),
    path("result_list/",result_list,name="result_list"),
    path("result_detail/",result_detail,name="result_detail"),
    path("gift_complete/",gift_complete,name="gift_complete"),
    path("create_payment/",create_payment,name="create_payment"),
    path("create_gift/",create_gift,name="create_gift"),
]
