from django.shortcuts import render, get_object_or_404, redirect
from admin_module.forms import OIRateForm
from admin_module.models import City, OIRate


def oi_rates(request):
    oi_rates_data = OIRate.objects.all()
    cities = City.objects.all()
    if request.method == 'POST':
        form = OIRateForm(request.POST)
        if form.is_valid():
            oi_rates = form.save(commit=False)
            oi_rates.created_by = request.user.username
            oi_rates.modified_by = request.user.username
            oi_rates.save()
            return redirect('admin_module:oi_rates')

    else:
        form = OIRateForm()

    return render(request, 'dictionaries/oi_rates.html',{'oi_rates_data':oi_rates_data,'cities': cities})

def edit_oi_rates(request, oi_rates_id):
    oi_rates = get_object_or_404(OIRate, pk=oi_rates_id)

    if request.method == 'POST':
        form = OIRateForm(request.POST, instance=oi_rates)
        if form.is_valid():
            oi_rates = form.save(commit=False)
            oi_rates.modified_by = request.user.username
            oi_rates.save()
            return redirect('admin_module:oi_rates')

    else:
        form = OIRateForm(instance=oi_rates)

    return render(request, 'dictionaries/edit_oi_rates.html', {'oi_rates': oi_rates, 'form': form})

def delete_oi_rates(request, oi_rates_id):
    oi_rates = get_object_or_404(OIRate, pk=oi_rates_id)

    if request.method == 'POST':
        oi_rates.delete()
        return redirect('admin_module:oi_rates')

    return render(request, 'dictionaries/delete_oi_rates.html', {'oi_rates': oi_rates})