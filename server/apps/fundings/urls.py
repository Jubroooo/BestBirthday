from django.urls import path
from .views import *

app_name = 'fundings'

urlpatterns = [
    path('', main, name="main"),
    path('create/', create, name="create"),
    # path('detail/<int:pk>/', detail, name="detail"), 
    path('delete/<int:pk>/', delete, name="delete"), 
    path('update/<int:pk>/', update, name="update"),
    path('detail/<int:pk>/message_create/', create_message, name="create_message"),
    path('list/today_funding/', today_funding, name="today_funding"),
    path('list/msg_funding/', msg_funding, name="msg_funding"),
    path('list/open_funding/', open_funding, name="open_funding"),
    path('view_messages/<int:pk>/', view_messages, name="view_messages"),
    path('view_all_messages/<int:pk>/', view_all_messages, name="view_all_messages"),
    path('funding_msg_detail/<int:pk>/', funding_msg_detail, name="funding_msg_detail"),
    path('message/create', message, name="message"),
    # 예진 추가뷰
    path('all_birthday_list/',all_list),
    #뷰 확인용
    path('detail/', detail, name="detail"),
]
