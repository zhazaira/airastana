from django.utils import timezone
from admin_module.models import Currency
from django.shortcuts import redirect, render,get_object_or_404


def currencies(request):
    currencies_data = Currency.objects.all()

    if request.method == 'POST':
        code = request.POST.get('code')
        full_name = request.POST.get('full_name')
        created_by = request.user.username
        modified_by = request.user.username
        created_date = timezone.now()
        modified_date = timezone.now()

        new_currency = Currency(code=code, full_name=full_name, created_by=created_by, modified_by=modified_by, created_date=created_date, modified_date=modified_date)
        new_currency.save()
        return redirect('admin_module:currencies')

    return render(request, 'dictionaries/currencies.html', {'currencies_data': currencies_data})


def delete_currency(request, currency_id):
    currency = get_object_or_404(Currency, pk=currency_id)
    if request.method == 'POST':
        currency.delete()
        return redirect('admin_module:currencies')

    return render(request, 'dictionaries/delete_currency.html', {'currency': currency})


def edit_currency(request, currency_id):
    currency = get_object_or_404(Currency, pk=currency_id)
    if request.method == 'POST':
        currency.code = request.POST.get('code')
        currency.full_name = request.POST.get('full_name')
        currency.modified_by = request.user.username
        currency.save()
        return redirect('admin_module:currencies')

    return render(request, 'dictionaries/edit_currency.html', {'currency': currency})



