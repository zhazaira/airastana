from django.urls import path
from . import views_city, views_currency, views_admin, views, views_gpa_code, views_subclass, views_commission, \
    views_exchange, views_kzd_rates, views_oi_rates, views_sdr_rates

app_name = 'admin_module'
urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main, name='main'),
    path('login/', views.login_view, name='login'),
    path('dictionaries/', views.dictionaries_view, name='dictionaries'),
    
    path('records/',views.records, name="records"),
    path('reports/',views.reports, name="reports"),
    path('reports/cn51',views.report_cn51, name="report_cn51"),
    path('calculate_cost/', views.calculate_cost, name='calculate_cost'),

    path('add_user/', views_admin.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', views_admin.edit_user, name='edit_user'),
    path('block_user/<int:user_id>/', views_admin.block_user, name='block_user'),
    path('user_list/', views_admin.user_list, name='user_list'),


    path('cities/', views_city.cities, name='cities'),
    path('cities/edit/<int:city_id>/', views_city.edit_city, name='edit_city'),
    path('cities/delete/<int:city_id>/', views_city.delete_city, name='delete_city'),
    path('upload_excel_cities', views_city.upload_excel_cities, name="upload_excel_cities"),
    
    path('currencies/', views_currency.currencies, name="currencies"),
    path('currencies/edit/<int:currency_id>/', views_currency.edit_currency, name='edit_currency'),
    path('currencies/delete/<int:currency_id>/', views_currency.delete_currency, name='delete_currency'),


    path('exchange_rates/', views_exchange.exchange_rates, name='exchange_rates'),
    path('delete_exchange_rate/<int:exchange_rate_id>/', views_exchange.delete_exchange_rate, name="delete_exchange_rate"),


    path('gpa_code/', views_gpa_code.gpa_code, name="gpa_code"),
    path('gpa_code/edit/<int:gpa_code_id>/', views_gpa_code.edit_gpa_code, name='edit_gpa_code'),
    path('gpa_code/delete/<int:gpa_code_id>/', views_gpa_code.delete_gpa_code, name='delete_gpa_code'),

    path('subclass/', views_subclass.subclass, name="subclass"),
    path('edit_subclass/<int:subclass_id>/', views_subclass.edit_subclass, name="edit_subclass"),
    path('delete_subclass/<int:subclass_id>/', views_subclass.delete_subclass, name="delete_subclass"),

    path('commission', views_commission.commission, name='commission'),
    path('commission/edit/<int:commission_id>/', views_commission.edit_commission, name='edit_commission'),
    path('commission/delete/<int:commission_id>/', views_commission.delete_commission, name='delete_commission'),

    path('kzd_rates', views_kzd_rates.kzd_rates, name="kzd_rates"),
    path('edit_kzd_rate/<int:kzd_rate_id>/', views_kzd_rates.edit_kzd_rate, name="edit_kzd_rate"),
    path('delete_kzd_rate/<int:kzd_rate_id>/', views_kzd_rates.delete_kzd_rate, name="delete_kzd_rate"),
    path('upload_excel', views_kzd_rates.upload_excel, name="upload_excel"),
    
    path('oi_rates', views_oi_rates.oi_rates, name="oi_rates"),
    path('oi_rates/edit/<int:oi_rates_id>/', views_oi_rates.edit_oi_rates, name='edit_oi_rates'),
    path('oi_rates/delete/<int:oi_rates_id>/', views_oi_rates.delete_oi_rates, name='delete_oi_rates'),

    path('sdr_rates/', views_sdr_rates.sdr_rates, name='sdr_rates'),
    path('sdr_rates/edit/<int:sdr_rates_id>/', views_sdr_rates.edit_sdr_rates, name='edit_sdr_rates'),
    path('sdr_rates/delete/<int:sdr_rates_id>/', views_sdr_rates.delete_sdr_rates, name='delete_sdr_rates'),
    path('upload_excel_sdr', views_sdr_rates.upload_excel_sdr, name="upload_excel_sdr"),

]
