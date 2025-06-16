from django import forms  
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from coffee.views import *
#from coffee.scripts import monthSales, popMenu, topMenu, bestPlaces

class authForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]
   
class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Начальная дата"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Конечная дата"
    )

