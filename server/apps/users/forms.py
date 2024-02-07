from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nickname', 'birthday']
        
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'birthday', 'profile']
    nickname = forms.CharField(label='닉네임', max_length=24, required=True)
    birthday = forms.DateField(label='생일', required=True)
    
    
class kakaoForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['kakao_account']
        
class tossForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['toss_account']
    