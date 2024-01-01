from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
import openpyxl
from admin_module.models import City
from admin_module.forms import ExcelUploadForm
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404


def cities(request):
    cities_data = City.objects.all()
    if request.method == 'POST':
        city_code = request.POST.get('city_code')
        city_name = request.POST.get('city_name')
        created_by = request.user.username
        modified_by = request.user.username
        created_date = timezone.now()
        modified_date = timezone.now()

        new_city: City = City(city_code=city_code, city_name=city_name, created_by=created_by, modified_by=modified_by, created_date=created_date, modified_date=modified_date)
        new_city.save()
        return redirect('admin_module:cities')

    return render(request, 'dictionaries/cities.html', {'cities_data': cities_data})


def edit_city(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    if request.method == 'POST':
        city.city_code = request.POST.get('city_code')
        city.city_name = request.POST.get('city_name')
        city.modified_by = request.user.username
        city.save()
        return redirect('admin_module:cities')

    return render(request, 'dictionaries/edit_city.html', {'city': city})


def delete_city(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    if request.method == 'POST':
        city.delete()
        return redirect('admin_module:cities')

    return render(request, 'dictionaries/delete_city.html', {'city': city})


def upload_excel_cities(request):
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
                        id, city_code, city_name, is_removed  = row
                        

                        
                        if City.objects.filter(city_code=city_code).count() == 0:
                                City.objects.create(
                                    city_code=city_code,
                                    city_name=city_name,
                                    created_by = request.user,
                                    modified_by = request.user
                                )

                    return HttpResponseRedirect(reverse('admin_module:cities'))
                except Exception as e:
                    print(str(e))
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                return JsonResponse(
                    {'success': False, 'error': 'Invalid file format. Please upload an Excel file (.xlsx).'})
    else:
        form = ExcelUploadForm()

    return render(request, 'dictionaries/cities.html', {'form': form})