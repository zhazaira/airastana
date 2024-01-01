from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import LoginForm,ExcelImportForm
import pandas as pd
from django.utils import timezone
from .models import *
from datetime import datetime
from reportlab.pdfgen import canvas
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Spacer,Paragraph
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle


def records(request):
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # Process DataFrame and save to the database
            for index, row in df.iterrows():
                Records.objects.create(
                    GPACode=row['GPACode'],
                    Origin=row['Origin'],
                    Destination=row['Destination'],
                    Subclass=row['Subclass'],
                    Flight1=row['Flight1'],
                    FltDate=row['FltDate'],
                    Wgt=row['Wgt'],
                    Depeche=row['Depeche'],
                    GroupDate=row['Group Date'],
                    created_by=request.user.username,
                    modified_by=request.user.username,
                    created_date = timezone.now(),
                    modified_date = timezone.now()
                )

            # Redirect to the records page
            return redirect('admin_module:records')

    else:
        form = ExcelImportForm()

    # Retrieve all records from the Report model
    records = Records.objects.all()

    # Pass the records and form to the template
    return render(request, 'admin_module/records.html', {'records': records, 'form': form})

def calculate_cost(request):
    # Получаем все записи, где Origin = 'ALA' и Destination = 'FRU'
    records = Records.objects.filter(Origin='ALA', Destination='FRU')

    # Получаем тариф для ALA -> FRU
    tariff = SdrRate.objects.filter(city_1__city_code='ALA', city_2__city_code='FRU').first()

    if tariff is not None:
        # Рассчитываем общую стоимость
        total_cost = records.aggregate(Sum('Wgt'))['Wgt__sum'] * tariff.rate
    else:
        total_cost = None

    # Получаем данные из записи Records
    records_data = Records.objects.filter(Origin='ALA', Destination='FRU').first()

    # Получаем данные из записи SdrRate
    sdr_rate_data = SdrRate.objects.filter(city_1__city_code='ALA', city_2__city_code='FRU').first()

    # Создаем PDF-документ с результатами
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cost_calculation.pdf"'

    # Устанавливаем размер страницы
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Определяем столбцы и строки для таблицы
    columns = ["Parcours pats de destination ou groupes",
               "Categones d'envos",
               "Poids transpote au cors du ou des mois",
               "Poids total",
               "Prix du transport par kg",
               "Total des frais de transport a paye"]

    data = [
        ["1", "2", "3", "4", "5", "6"],
        ["", "Prioritaire", "kg", "kg", "SDR", "SDR"],
        ["ALA_FRU", "CP",
         str(records_data.Wgt) if records_data else "N/A",
         str(records_data.Wgt) if records_data else "N/A",
         str(sdr_rate_data.rate) if sdr_rate_data else "N/A",
         f"{total_cost:.2f}" if total_cost is not None else "N/A"],
        ["Total general", "", ""]
    ]

    # Формируем таблицу
    table_data = [columns] + data
    table = Table(table_data, colWidths=[100] * len(columns))

    # Настраиваем стиль таблицы
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Получаем стиль 'Heading2'
    heading2_style = getSampleStyleSheet()['Heading2']

    # Собираем документ
    elements = [
    table, Spacer(1, 12), Spacer(1, 12),
    Spacer(1, 6),
    Paragraph(
        "<u>Administration creancire</u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<u>Vue et accepte par l'Administration debitrice</u>",
        style=ParagraphStyle(
            'Heading2',
            fontSize=10,
            spaceBefore=100,
            spaceAfter=6,
        )
    ),

    Paragraph(
            "<u>Signature</u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<u>Lieu,date et signature</u>",

              style=ParagraphStyle(
                  'Heading2',
                  fontSize=10,
                  spaceBefore=6,
                  spaceAfter=6,
              )
              )
]

    pdf.build(elements)


    return response


def home(request):
    return render(request, 'admin_module/admin_home.html')


def main(request):
    return render(request, 'admin_module/main.html')   

def reports(request):
    return render(request, 'admin_module/reports.html')   

def report_cn51(request):
    return render(request, 'admin_module/report_cn51.html')   


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_module:main')
    else:
        form = LoginForm()

    return render(request, 'admin_module/login.html', {'form': form})


def dictionaries_view(request):
    return render(request, 'admin_module/dictionaries.html')
