
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import UserProfile, ExchangeRate, Currency, SdrRate, GPACode, Subclass
from .forms import UserForm, UserProfileForm,  CurrencyForm, AddExchangeRateForm, UploadExcelForm, GPACodeForm,SubclassForm
from django.contrib.auth.decorators import login_required
from .models import City
import pandas as pd

@login_required
@staff_member_required
def add_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Сохранение данных пользователя и профиля
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # Дополнительные действия после создания пользователя
            return redirect('admin_module:user_list')  # Перенаправление после успешного создания пользователя
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'admin_module/add_user.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
@staff_member_required
def edit_user(request, user_id):
    # Извлечение пользователя и связанного с ним профиля из базы данных
    try:
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        # Обработка случая, когда пользователь с предоставленным user_id не существует
        return HttpResponse("Пользователь не найден", status=404)

    if request.method == 'POST':
        # Обработка отправки формы для обновления данных пользователя и профиля
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('admin_module:user_list')  # Перенаправление на страницу списка пользователей после успешного редактирования
    else:
        # Отображение данных пользователя и профиля для редактирования
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'admin_module/edit_user.html', {'user_form': user_form, 'profile_form': profile_form, 'user': user})


@login_required
@staff_member_required
def block_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_home') 


def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'admin_module/user_list.html', {'users': users})


def dictionaries_view(request):
    return render(request, 'admin_module/dictionaries.html')


def sdr_rates(request):
    sdr_rates_data = SdrRate.objects.all()
    return render(request, 'dictionaries/sdr_rates.html', {'sdr_rates_data':sdr_rates_data})


def cities(request):
    cities_data = City.objects.all()
    if request.method == 'POST':
        city_code = request.POST.get('city_code')
        city_name = request.POST.get('city_name')
        created_by = request.user.username
        modified_by = request.user.username
        created_date = timezone.now()
        modified_date = timezone.now()

        new_city = City(city_code=city_code, city_name=city_name, created_by=created_by, modified_by=modified_by, created_date=created_date, modified_date=modified_date)
        new_city.save()
        return redirect('admin_module:cities')
        return render(request, 'dictionaries/cities.html', {'cities_data': cities_data})


def edit_city(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    if request.method == 'POST':
        city.city_code = request.POST.get('city_code')  # или другое значение по умолчанию, если ключ отсутствует
        city.city_name = request.POST.get('city_name')
        city.modified_by = request.user.username  # или другой способ получения имени пользователя
        city.save()
        return redirect('admin_module:cities')

    return render(request, 'dictionaries/edit_city.html', {'city': city})


def delete_city(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    if request.method == 'POST':
        city.delete()
        return redirect('admin_module:cities')

    return render(request, 'dictionaries/delete_city.html', {'city': city})


def currencies(request):
    currencies_data = Currency.objects.all()
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_module:currencies')

    else:
        form = CurrencyForm()

    return render(request, 'dictionaries/currencies.html', {'currencies_data': currencies_data, 'form': form})


def add_currency(request):
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_module:currencies')
    else:
        form = CurrencyForm()
    return render(request, 'dictionaries/currencies.html', {'form': form})


def delete_currency(request, currency_id):
    currency = get_object_or_404(Currency, pk=currency_id)
    if request.method == 'POST':
        currency.delete()
        return redirect('admin_module:currencies')

    return render(request, 'dictionaries/delete_currency.html', {'currency': currency})


def edit_currency(request, currency_id):
    currency = get_object_or_404(Currency, pk=currency_id)
    if request.method == 'POST':
        currency.code = request.POST.get('code')  # или другое значение по умолчанию, если ключ отсутствует
        currency.full_name = request.POST.get('full_name')
        currency.modified_by = request.user.username  # или другой способ получения имени пользователя
        currency.save()
        return redirect('admin_module:currencies')

    return render(request, 'dictionaries/edit_currency.html', {'currency': currency})


def gpa_code(request):
    gpa_code_data = GPACode.objects.all()
    currency_data = Currency.objects.all()

    if request.method == 'POST':
        form = GPACodeForm(request.POST)
        if form.is_valid():
            gpa_code = form.save(commit=False)
            gpa_code.created_by = request.user.username
            gpa_code.modified_by = request.user.username
            gpa_code.save()
            return redirect('admin_module:gpa_code')

    else:
        form = GPACodeForm()

    return render(request, 'dictionaries/gpa_code.html', {'gpa_code_data': gpa_code_data, 'form': form, 'currency_data': currency_data})


def edit_gpa_code(request, gpa_code_id):
    gpa_code = get_object_or_404(GPACode, pk=gpa_code_id)
    currency_data = Currency.objects.all()

    if request.method == 'POST':
        form = GPACodeForm(request.POST, instance=gpa_code)
        if form.is_valid():
            gpa_code.modified_by = request.user.username
            form.save()
            return redirect('admin_module:gpa_code')

    else:
        form = GPACodeForm(instance=gpa_code)

    return render(request, 'dictionaries/gpa_code_edit.html',
                  {'gpa_code': gpa_code, 'form': form, 'currency_data': currency_data})


def delete_gpa_code(request, gpa_code_id):
    gpa_code = get_object_or_404(GPACode, pk=gpa_code_id)

    if request.method == 'POST':
        gpa_code.delete()
        return redirect('admin_module:gpa_code')

    return render(request, 'dictionaries/gpa_code_delete.html', {'gpa_code': gpa_code})


def subclass(request):
    subclass_data = Subclass.objects.all()
    if request.method == 'POST':
        form = SubclassForm(request.POST)
        if form.is_valid():
            subclass = form.save(commit=False)
            subclass.created_by = request.user.username
            subclass.modified_by = request.user.username
            form.save()
        return redirect('admin_module:subclass')
    else:
        form = SubclassForm()

    return render(request, 'dictionaries/subclass.html', {'subclass_data': subclass_data, 'form': form,})


def edit_subclass(request, subclass_id):
    subclass = get_object_or_404(Subclass, pk=subclass_id)
    subclass_data = Subclass.objects.all()

    if request.method == 'POST':
        form = SubclassForm(request.POST, instance=subclass)
        if form.is_valid():
            subclass = form.save(commit=False)
            subclass.modified_by = request.user.username
            form.save()
            return redirect('admin_module:subclass')

    else:
        form = SubclassForm(instance=subclass)

    return render(request, 'dictionaries/edit_subclass.html',
                  {'subclass': subclass, 'form': form})


def delete_subclass(request, subclass_id):
    subclass = get_object_or_404(Subclass, pk=subclass_id)

    if request.method == 'POST':
        subclass.delete()
        return redirect('admin_module:subclass')

    return render(request, 'dictionaries/delete_subclass.html', {'subclass': subclass})


def delete_exchange_rate(request, exchange_rate_id):
    if request.method == 'POST':
        try:
            exchange_rate = ExchangeRate.objects.get(id=exchange_rate_id)
            exchange_rate.delete()
            return JsonResponse({'success': True})
        except ExchangeRate.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Курс обмена не найден'})

    return JsonResponse({'success': False, 'error': 'Недопустимый метод запроса'})


def exchange_rates(request, upload_form=None):
    if request.method == 'POST':
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            if excel_file.name.endswith('.xlsx'):
                data = pd.read_excel(excel_file)

                for index, row in data.iterrows():
                    rate_1_name = row['Валюта 1']
                    rate_2_name = row['Валюта 2']

                    try:
                        rate_1 = Currency.objects.get(code=rate_1_name)
                    except Currency.DoesNotExist:
                        rate_1 = Currency(code=rate_1_name, full_name=rate_1_name)
                        rate_1.save()

                    try:
                        rate_2 = Currency.objects.get(code=rate_2_name)
                    except Currency.DoesNotExist:
                        rate_2 = Currency(code=rate_2_name)
                        rate_2.save()

                    exchange_rate = ExchangeRate(
                        rate_1=rate_1,
                        rate_2=rate_2,
                        value=row['Значение'],
                        created_by=request.user.username,
                        modified_by=request.user.username,
                    )
                    exchange_rate.save()


                return redirect('admin_module:exchange_rates')
            else:

                return redirect('admin_module:exchange_rates')

        else:
            form = AddExchangeRateForm(request.POST)
            if form.is_valid():
                value = form.cleaned_data['value']
                rate_1 = form.cleaned_data['rate_1']
                rate_2 = form.cleaned_data['rate_2']
                created_by = request.user.username
                modified_by = request.user.username

                exchange_rate = ExchangeRate(
                    rate_1=rate_1,
                    rate_2=rate_2,
                    value=value,
                    created_by=request.user.username,
                    modified_by=request.user.username,
                )
                exchange_rate.save()

                return redirect('admin_module:exchange_rates')

    else:
        upload_form = UploadExcelForm()
        form = AddExchangeRateForm()

    exchange_rates_data = ExchangeRate.objects.all()

    return render(request, 'dictionaries/exchange_rates.html', {
        'exchange_rates_data': exchange_rates_data,
        'upload_form': upload_form,
        'form': form,
    })
