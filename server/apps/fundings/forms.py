from django import forms
from .models import *

class FundingForm(forms.ModelForm):
    class Meta():
        model = Funding
        fields = ['title', 'photo', 'content', 'goal_price', 'present_link'] 

    def save(self, commit=True, user=None):
        # 유저는 현재 요청하는 유저로
        if user:
            self.instance.user = user
        else:
            self.instance.user = self.request.user

        return super().save(commit=commit)
    
class MessageForm(forms.ModelForm):
    class Meta():
        model = Funding_Msg
        fields = ['comment_name', 'content', 'funding_price']
    
    def __init__(self, *args, **kwargs):
        # Get the request and current_post from the kwargs during form initialization
        self.request = kwargs.pop('request', None)
        self.current_post = kwargs.pop('current_post', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Set the user field to the current user and post field to the current post
        self.instance.user = self.request.user
        self.instance.post = self.current_post

        return super().save(commit=commit)