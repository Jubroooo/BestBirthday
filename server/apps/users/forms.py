from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from datetime import datetime, date

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nickname', 'birthday']
        
class UserProfileUpdateForm(forms.ModelForm):
    birth_year = forms.IntegerField(label='출생 연도', required=True)
    birth_month = forms.IntegerField(label='출생 월', required=True)
    birth_day = forms.IntegerField(label='출생 일', required=True)

    class Meta:
        model = User
        fields = ['nickname', 'profile']

    def clean_birthday(self):
        birth_year = self.cleaned_data.get('birth_year')
        birth_month = self.cleaned_data.get('birth_month')
        birth_day = self.cleaned_data.get('birth_day')
        
        try:
            birthday = date(birth_year, birth_month, birth_day)
        except ValueError:
            raise forms.ValidationError("올바른 날짜를 선택해주세요.")

        return birthday

    def save(self, commit=True):
        user = super(UserProfileUpdateForm, self).save(commit=False)

        #생일 합치기
        birth_year = self.cleaned_data.get('birth_year')
        birth_month = self.cleaned_data.get('birth_month')
        birth_day = self.cleaned_data.get('birth_day')
        user.birthday = date(birth_year, birth_month, birth_day)

        if commit:
            user.save()

        return user

class UserProfilesettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'profile']

    
class kakaoForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['kakao_account']
        
class tossForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['toss_account']
    