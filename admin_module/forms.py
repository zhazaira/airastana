from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, City, Currency, ExchangeRate, GPACode, Subclass, Commission, KZDRate, OIRate, SdrRate


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


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
        fields = ['gpa_code', 'description', 'gpa_full_name', 'oracle_code', 'currency']


class SubclassForm(forms.ModelForm):
    class Meta:
        model = Subclass
        fields = ['name_code', 'name_description']



class CommissionForm(forms.ModelForm):
    gpa = forms.ModelChoiceField(queryset=GPACode.objects.all())  
    class Meta:
        model = Commission
        fields = ['gpa', 'value']


class KZDRateForm(forms.ModelForm):
    city_1 = forms.ModelChoiceField(queryset=City.objects.all())
    city_2 = forms.ModelChoiceField(queryset=City.objects.all())

    class Meta:
        model = KZDRate
        fields = '__all__'
        widgets = {
            'date_begin': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
        }


class OIRateForm(forms.ModelForm):
    city_1 = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Select City 1"),
    city_2 = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Select City 2")
    class Meta:
        model = OIRate
        fields = ['city_1', 'city_2', 'gpa_id', 'rate','date_begin', 'date_end']
        widgets = {
            'date_begin': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
        }



class SdrRateForm(forms.ModelForm):
    city_1 = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Select City 1"),
    city_2 = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Select City 2")

    class Meta:
        model = SdrRate
        fields = '__all__'
        widgets = {
            'date_begin': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}), }


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Select an Excel file')



class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()
    def clean_excel_file(self):
        excel_file = self.cleaned_data.get('excel_file')
        if excel_file:
            # Проверяем, является ли файл допустимым типом (например, .xls или .xlsx)
            allowed_extensions = ['.xls', '.xlsx']
            if not any(extension in excel_file.name for extension in allowed_extensions):
                raise forms.ValidationError('Пожалуйста, загрузите файл с расширением .xls или .xlsx.')

        return excel_file