from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, City, Currency, ExchangeRate, GPACode,Subclass


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('roles', 'status')



class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'


class AddExchangeRateForm(forms.ModelForm):
    value = forms.DecimalField(max_digits=10, decimal_places=5, label='Значение')
    rate_1 = forms.ModelChoiceField(queryset=Currency.objects.all(), label='Валюта 1')
    rate_2 = forms.ModelChoiceField(queryset=Currency.objects.all(), label='Валюта 2')

    class Meta:
        model = ExchangeRate
        fields = ('value', 'rate_1', 'rate_2', 'value')


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField()


class GPACodeForm(forms.ModelForm):
    class Meta:
        model = GPACode
        fields = ['gpa_code','description','gpa_full_name','oracle_code', 'currency']


class SubclassForm(forms.ModelForm):
    class Meta:
        model = Subclass
        fields = ['name_code','name_description']