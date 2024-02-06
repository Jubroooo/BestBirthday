from django.urls import path
from .views import *

app_name = 'fundings'

urlpatterns = [
    path('', main, name="main"),
    path('start/', start, name="start"),
    path('main_all_birthday_list/', main_all_birthday_list, name="main_all_birthday_list"),
    path('main_all_funding_list/', main_all_funding_list, name="main_all_funding_list"),
    path('main_ranking_list/', main_ranking_list, name="main_ranking_list"),
    path('detail/<int:pk>/', detail, name="detail"), 
    path('detail/<int:pk>/create_gift/', create_gift, name="create_gift"),
    path('detail/<int:pk>/create_gift_complete/', create_gift_complete, name="create_gift_complete"),
    path('detail/<int:pk>/create_gift_modal', create_gift_modal, name="create_gift_modal"),
    path('create_payment/', create_payment, name="create_payment"), 
    path('create_funding/', create_funding, name="create_funding"), 
    path('result_modal/<int:pk>/', result_modal, name="result_modal"), 
    path('result_start/<int:pk>/', result_start, name="result_start"), 
    path('result_detail/<int:pk>/', result_detail, name="result_detail"), 
    path('result_start/', result_start, name="result_start"), 
 
     path('mypage_list/', mypage_list, name="mypage_list"), 
     path('mypage_profile_setting/', mypage_profile_setting, name="mypage_profile_setting"), 
     path('mypage_payment_guide_k/', mypage_payment_guide_k, name="mypage_payment_guide_k"), 
     path('mypage_payment_guide_t/', mypage_payment_guide_t, name="mypage_payment_guide_t"), 
     path('mypage_myfunding/', mypage_myfunding, name="mypage_myfunding"), 
     path('mypage_participated/', mypage_participated, name="mypage_participated"),
]
