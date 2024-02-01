from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'nickname', 'birthday']
        
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'nickname', 'birthday', 'profile']
        
    name = forms.CharField(label='이름', max_length=10, required=True)
    nickname = forms.CharField(label='닉네임', max_length=24, required=True)
    birthday = forms.DateField(label='생일', required=True)
    