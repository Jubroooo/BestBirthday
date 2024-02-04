from django.urls import path
from .views import *

app_name = 'fundings'

urlpatterns = [
    path('', main, name="main"),
    #path('start/', start, name="start"),
    path('main_all_birthday_list/', main_all_birthday_list, name="main_all_birthday_list"),
    path('main_all_funding_list/', main_all_funding_list, name="main_all_funding_list"),
    path('main_ranking_list/', main_ranking_list, name="main_ranking_list"),
    # path('detail/<int:pk>/', detail, name="detail"), 
    path('detail/<int:pk>/', detail, name="detail"), 
    path('detail/<int:pk>/create_gift/', create_gift, name="create_gift"),
    path('detail/<int:pk>/create_gift_complete/', create_gift_complete, name="create_gift_complete"),
    path('detail/<int:pk>/create_gift_modal', create_gift_modal, name="create_gift_modal"),
    path('create_payment/', create_payment, name="create_payment"), 
    path('create_funding/', create_funding, name="create_funding"), 
    #path('result_modal/', result_modal, name="result_modal"), 
    path('result_start/<int:pk>/', result_start, name="result_start"), 
    path('result_list/<int:pk>/', result_list, name="result_list"), 
    path('result_detail/<int:pk>/', result_detail, name="result_detail"), 
    #--------------------------------------마이페이지 관련
    # path('mypage_list/', mypage_list, name="mypage_list"), 
    # path('mypage_profile_setting/', mypage_profile_setting, name="mypage_profile_setting"), 
    # path('mypage_payment_guide/', mypage_payment_guide, name="mypage_payment_guide"), 
    # path('mypage_myfunding/', mypage_myfunding, name="mypage_myfunding"), 
    # path('mypage_participated/', mypage_participated, name="mypage_participated"),


    # 채연 추가뷰
    path('detail/', detail, name="detail"),
    path('my_detail/', my_detail, name="my_detail"),
    path("result_modal/",result_modal,name="result_modal"),
    path("result_start/",result_start,name="result_start"),
    #합쳐서 이제 필요 없음path("result_list/",result_list,name="result_list"),
    path("result_detail/",result_detail,name="result_detail"),
    path("gift_complete/",gift_complete,name="gift_complete"),
    path("create_gift/",create_gift,name="create_gift"),
]
