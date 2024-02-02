from django import forms
from .models import *

class FundingForm(forms.ModelForm):
    class Meta():
        model = Funding
        fields = ['title', 'photo', 'content', 'goal_price', 'present_link'] 

class MessageForm(forms.ModelForm):
    class Meta():
        model = Funding_Msg
        fields = ['comment_name', 'content', 'funding_price']