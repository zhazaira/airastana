from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from admin_module.forms import SdrRateForm, ExcelUploadForm
from admin_module.models import SdrRate, City
from django.urls import reverse
import openpyxl

def sdr_rates(request):
    sdr_rates_data = SdrRate.objects.all()
    cities = City.objects.all()
    if request.method == 'POST':
        form = SdrRateForm(request.POST)
        if form.is_valid():
            sdr_rates = form.save(commit=False)
            sdr_rates.created_by = request.user.username
            sdr_rates.modified_by = request.user.username
            sdr_rates.save()
            return redirect('admin_module:sdr_rates')

    else:
        SdrRateForm()
    return render(request, 'dictionaries/sdr_rates.html', {'sdr_rates_data': sdr_rates_data, 'cities': cities})


def edit_sdr_rates(request, sdr_rates_id):
    sdr_rates = get_object_or_404(SdrRate, pk=sdr_rates_id)

    if request.method == 'POST':
        form = SdrRateForm(request.POST, instance=sdr_rates)
        if form.is_valid():
            sdr_rates = form.save(commit=False)
            sdr_rates.modified_by = request.user.username
            sdr_rates.save()
            return redirect('admin_module:sdr_rates')

    else:
        form = SdrRateForm(instance=sdr_rates)

    return render(request, 'dictionaries/edit_sdr_rates.html', {'sdr_rates': sdr_rates, 'form': form})


def delete_sdr_rates(request, sdr_rates_id):
    sdr_rates = get_object_or_404(SdrRate, pk=sdr_rates_id)

    if request.method == 'POST':
        sdr_rates.delete()
        return redirect('admin_module:sdr_rates')

    return render(request, 'dictionaries/delete_sdr_rates.html', {'sdr_rates': sdr_rates})


def upload_excel_sdr(request):
    if request.method == 'POST':

        if 2 + 2 == 4:
            excel_file = request.FILES['excel_file']
            print("22")
            if excel_file.name.endswith('.xlsx'):
                print("33")
                try:
                    workbook = openpyxl.load_workbook(excel_file)
                    worksheet = workbook.active

                    for row in worksheet.iter_rows(min_row=2, values_only=True):
                        print("44")
                        city_1, city_2, rate, date_begin, date_end, lub, luo = row
                        print(rate)
                        cityy1=City.objects.get(city_code=city_1)
                        cityy2=City.objects.get(city_code=city_2)

                        date_begin_parsed = f"{date_begin[6:]}-{date_begin[3:5]}-{date_begin[:2]}"
                        date_end_parsed = f"{date_end[6:]}-{date_end[3:5]}-{date_end[:2]}"

                        if SdrRate.objects.filter(city_1=cityy1).filter(city_2=cityy2).count() == 0:
                                SdrRate.objects.create(
                                    city_1=cityy1,
                                    city_2=cityy2,
                                    date_begin=date_begin_parsed,
                                    rate = rate,
                                    date_end =date_end_parsed, 
                                    created_by = request.user,
                                    modified_by = request.user
                                )

                    return HttpResponseRedirect(reverse('admin_module:sdr_rates'))
                except Exception as e:
                    print(str(e))
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                return JsonResponse(
                    {'success': False, 'error': 'Invalid file format. Please upload an Excel file (.xlsx).'})
    else:
        form = ExcelUploadForm()

    return render(request, 'dictionaries/sdr_rates.html', {'form': form})