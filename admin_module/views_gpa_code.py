from admin_module.forms import GPACodeForm
from admin_module.models import GPACode, Currency
from django.shortcuts import redirect, render, get_object_or_404


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