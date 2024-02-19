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

    def clean(self):
        cleaned_data = super().clean()
        birth_year = cleaned_data.get('birth_year')
        birth_month = cleaned_data.get('birth_month')
        birth_day = cleaned_data.get('birth_day')

        if not self.is_valid_birthday(birth_year, birth_month, birth_day):
            raise forms.ValidationError("올바른 날짜를 선택해주세요.")

    def is_valid_birthday(self, year, month, day):
        # 여기서 생일의 유효성 검사를 수행합니다.
        # 예를 들어, 실제로 존재하는 날짜인지 확인하는 로직을 추가합니다.
        # 이 예시에서는 간단한 범위 검사를 수행하도록 했습니다.
        try:
            birthday = datetime(year, month, day)
            return True
        except ValueError:
            return False  # 잘못된 날짜 형식일 경우 False 반환
    
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
    