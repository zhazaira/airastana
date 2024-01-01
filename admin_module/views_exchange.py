import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render,redirect

from admin_module.forms import AddExchangeRateForm, UploadExcelForm
from admin_module.models import ExchangeRate, Currency


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

