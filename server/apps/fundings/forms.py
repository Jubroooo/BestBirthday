from django import forms
from .models import *

class FundingForm(forms.ModelForm):
    class Meta():
        model = Funding
        fields = ['title', 'photo', 'content', 'goal_price', 'present_link'] 

class MessageForm(forms.ModelForm):
    class Meta():
        model = Funding_Msg
        fields = ['funding_price', 'comment_name', 'content']
        
    def clean_funding_price(self):
        funding_price = self.cleaned_data.get('funding_price')
        if funding_price is not None and funding_price < 0:
            raise forms.ValidationError("펀딩 금액은 음수가 될 수 없습니다.")
        return funding_price
       
