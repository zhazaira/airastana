from django.urls import path
from . import views
app_name = 'admin_module'
urlpatterns = [
    path('dictionaries/', views.dictionaries_view, name='dictionaries'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('user_list/', views.user_list, name='user_list'),

    path('exchange_rates/', views.exchange_rates, name='exchange_rates'),
    path('sdr_rates/', views.sdr_rates, name='sdr_rates'),

    path('cities/', views.cities, name='cities'),
    path('cities/edit/<int:city_id>/', views.edit_city, name='edit_city'),
    path('cities/delete/<int:city_id>/', views.delete_city, name='delete_city'),
    
    path('currencies/', views.currencies,name="currencies"),
    path('currencies/edit/<int:currency_id>/', views.edit_currency, name='edit_currency'),
    path('currencies/delete/<int:currency_id>/', views.delete_currency, name='delete_currency'),
    path('add_currency/', views.add_currency, name='add_currency'),

    path('exchange_rates/', views.exchange_rates, name='exchange_rates'),
    path('delete_exchange_rate/<int:exchange_rate_id>/', views.delete_exchange_rate, name='delete_exchange_rate'),

    path('gpa_code/', views.gpa_code, name="gpa_code"),
    path('gpa_code/edit/<int:gpa_code_id>/', views.edit_gpa_code, name='edit_gpa_code'),
    path('gpa_code/delete/<int:gpa_code_id>/', views.delete_gpa_code, name='delete_gpa_code'),

    path('subclass/',views.subclass, name="subclass"),
    path('edit_subclass/<int:subclass_id>/',views.edit_subclass, name="edit_subclass"),
    path('delete_subclass/<int:subclass_id>/',views.delete_subclass,name="delete_subclass"),


]






