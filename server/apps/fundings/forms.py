from django import forms
from .models import Funding

class FundingForm(forms.ModelForm):
    class Meta():
        model = Funding
        fields = ('__all__')    