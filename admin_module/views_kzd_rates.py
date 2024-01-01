from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from admin_module.forms import KZDRateForm, ExcelUploadForm
from admin_module.models import KZDRate, City
from django.urls import reverse
import openpyxl

def kzd_rates(request):
    kzd_rate_data = KZDRate.objects.all()
    cities = City.objects.all()
    
    if request.method == 'POST':
        form = KZDRateForm(request.POST)

        if form.is_valid():
            kzd_rate = form.save(commit=False)
            kzd_rate.created_by = request.user.username
            kzd_rate.modified_by = request.user.username
            # kzd_rate.date_begin = f"{kzd_rate.date_begin[6:]}-{kzd_rate.date_begin[3:5]}-{kzd_rate.date_begin[:2]}"
            # kzd_rate.date_end = f"{kzd_rate.date_end[6:]}-{kzd_rate.date_end[3:5]}-{kzd_rate.date_end[:2]}"
            kzd_rate.save()
        else:
            # Вывести ошибки валидации в терминал для отладки
            print(form.errors)
    else:
        form = KZDRateForm()

    return render(request, 'dictionaries/kzd_rates.html',
                  {'form': form, 'kzd_rate_data': kzd_rate_data, 'cities': cities})




def edit_kzd_rate(request, kzd_rate_id):
    kzd_rate = get_object_or_404(KZDRate, pk=kzd_rate_id)
    if request.method == 'POST':
        form = KZDRateForm(request.POST, instance=kzd_rate)
        if form.is_valid():
            kzd_rate = form.save(commit=False)
            kzd_rate.modified_by = request.user.username
            kzd_rate.save()
            return redirect('admin_module:kzd_rate')

    else:
        form = KZDRateForm(instance=kzd_rate)

    return render(request, 'dictionaries/edit_kzd_rate.html', {'kzd_rate': kzd_rate, 'form': form})


def delete_kzd_rate(request, kzd_rate_id):
    kzd_rate = get_object_or_404(KZDRate, pk=kzd_rate_id)
    if request.method == 'POST':
        kzd_rate.delete()
        return redirect('admin_module:kzd_rates')

    return render(request, 'dictionaries/delete_kzd_rate.html', {'kzd_rate': kzd_rate})


def upload_excel(request):
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
                        city1, city2, date_begin, date_end, rate_po, rate_nw, rate_ems = row

                        for city in [city1, city2]:
                            if City.objects.filter(city_code=city).count() == 0:
                                City.objects.create(
                                    city_code=city,
                                    city_name=city,
                                )

                        city1_obj = City.objects.get(city_code=city1)
                        city2_obj = City.objects.get(city_code=city2)

                        date_begin_parsed = f"{date_begin[6:]}-{date_begin[3:5]}-{date_begin[:2]}"
                        date_end_parsed = f"{date_end[6:]}-{date_end[3:5]}-{date_end[:2]}"

                        KZDRate.objects.create(
                            city_1=city1_obj,
                            city_2=city2_obj,
                            date_begin=date_begin_parsed,
                            date_end=date_end_parsed,
                            rate_po=rate_po,
                            rate_nw=rate_nw,
                            rate_ems=rate_ems,
                            created_by=request.user
                        )

                    return HttpResponseRedirect(reverse('admin_module:kzd_rates'))
                except Exception as e:
                    print(str(e))
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                return JsonResponse(
                    {'success': False, 'error': 'Invalid file format. Please upload an Excel file (.xlsx).'})
    else:
        form = ExcelUploadForm()

    return render(request, 'dictionaries/kzd_rates.html', {'form': form})