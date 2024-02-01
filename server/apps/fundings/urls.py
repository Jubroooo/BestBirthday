from django.urls import path
from .views import *

app_name = 'fundings'

urlpatterns = [
    path('', main, name="main"),
    path('create/', create, name="create"),
    path('detail/<int:pk>/', detail, name="detail"), 
    path('delete/<int:pk>/', delete, name="delete"), 
    path('update/<int:pk>/', update, name="update"),
    path('detail/<int:pk>/message_create/', create_message, name="create_message"),
]
