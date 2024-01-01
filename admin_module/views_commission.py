from django.shortcuts import redirect, render, get_object_or_404

from admin_module.forms import CommissionForm
from admin_module.models import Commission, GPACode


def commission(request):
    commission_data = Commission.objects.all()
    gpa_code = GPACode.objects.all()

    if request.method == 'POST':
        form = CommissionForm(request.POST)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.created_by = request.user.username
            commission.modified_by = request.user.username
            commission.save()
            return redirect('admin_module:commission')
    else:
        form = CommissionForm()

    # Обработка GET-запроса
    if request.method == 'GET':
        search_gpa = request.GET.get('search_gpa', '')  # Получите значение для поиска
        form = CommissionForm()  # Создайте форму для GET-запроса
        commission_data = Commission.objects.all()  # Получите данные, которые нужно отобразить
        gpa_code = GPACode.objects.all()  # Получите данные для выпадающего списка

        if search_gpa:
            # Если указан текст для поиска GPA, выполните фильтрацию
            commission_data = commission_data.filter(gpa__gpa_code__icontains=search_gpa)

    return render(request, 'dictionaries/commission.html',
                  {'form': form, 'commission_data': commission_data, 'gpa_code': gpa_code})


def edit_commission(request, commission_id):
    commission = get_object_or_404(Commission, pk=commission_id)

    if request.method == 'POST':
        form = CommissionForm(request.POST, instance=commission)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.modified_by = request.user.username
            commission.save()
            return redirect('admin_module:commission')

    else:
        form = CommissionForm(instance=commission)

    return render(request, 'dictionaries/edit_commission.html', {'commission': commission, 'form': form})


def delete_commission(request, commission_id):
    commission = get_object_or_404(Commission, pk=commission_id)

    if request.method == 'POST':
        commission.delete()
        return redirect('admin_module:commission')

    return render(request, 'dictionaries/delete_commission.html', {'commission': commission})