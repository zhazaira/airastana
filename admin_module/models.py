from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.CharField(max_length=255, choices=[
        ('Admin', 'Admin'),
        ('Senior', 'Senior'),
        ('User', 'User'),
    ])
    status = models.BooleanField(default=True)  # Поле для статуса пользователя
    password = models.CharField(max_length=255)  # Поле для хранения пароля

    def __str__(self):
        return self.user.username
    

class City(models.Model):
    city_code = models.CharField(max_length=255, verbose_name='Наименование', unique=True)
    city_name = models.CharField(max_length=255, verbose_name='Наименование города')
    created_by = models.CharField(max_length=10, verbose_name='Логин, кем создана запись')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    modified_by = models.CharField(max_length=10, verbose_name='Логин, вносивший изменение')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.city_code

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class Currency(models.Model):
    code = models.CharField(max_length=10, verbose_name='Сокращенное название валюты', unique=True)
    full_name = models.CharField(max_length=255, verbose_name='Полное название валюты')
    created_by = models.CharField(max_length=10, verbose_name='Логин, кем создана запись')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_by = models.CharField(max_length=10, verbose_name='Логин, вносивший изменение')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class GPACode(models.Model):
    gpa_code = models.CharField(max_length=255, verbose_name='Наименование', unique=True)
    description = models.CharField(max_length=255, verbose_name='Описание')
    gpa_full_name = models.CharField(max_length=255, verbose_name='Полное наименование')
    oracle_code = models.CharField(max_length=255, verbose_name='Код поставщика')
    created_by = models.CharField(max_length=10, verbose_name='Логин, кем создана запись')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Валюта')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_by = models.CharField(max_length=10, verbose_name='Логин, вносивший изменение')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.gpa_code

    class Meta:
        verbose_name = 'Код агента'
        verbose_name_plural = 'Коды агентов'


class SdrRate(models.Model):
    city_1 = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город 1', related_name='sdr_rates_city_1')
    city_2 = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город 2', related_name='sdr_rates_city_2')
    rate = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Тариф')
    date_begin = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')
    created_by = models.CharField(max_length=10, verbose_name='Логин, кем создана запись')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_by = models.CharField(max_length=10, verbose_name='Логин, вносивший изменение')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.city_1} - {self.city_2} ({self.date_begin} - {self.date_end})'

    class Meta:
        verbose_name = 'Тариф SDR'
        verbose_name_plural = 'Тарифы SDR'


class KZDRate(models.Model):
    city_1 = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город 1', related_name='kzd_rates_city_1')
    city_2 = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город 2', related_name='kzd_rates_city_2')
    date_begin = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')
    rate_po = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Тариф PO')
    rate_nw = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Тариф NW')
    rate_ems = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Тариф EMS')
    rate_eli = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Тариф ELI')
    created_by = models.CharField(max_length=10, verbose_name='Логин, кем создана запись')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_by = models.CharField(max_length=10, verbose_name='Логин, вносивший изменение')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.city_1} - {self.city_2} ({self.date_begin} - {self.date_end})'

    class Meta:
        verbose_name = 'Тариф KZD'
        verbose_name_plural = 'Тарифы KZD'


class OIRate(models.Model):
    city_1 = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город 1', related_name='oi_rates_city_1')
    city_2 = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город 2', related_name='oi_rates_city_2')
    gpa_id = models.CharField(max_length=255, verbose_name='GPA ID')
    rate = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Тариф')
    date_begin = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')
    created_by = models.CharField(max_length=10, verbose_name='Логин, кем создана запись')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_by = models.CharField(max_length=10, verbose_name='Логин, вносивший изменение')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.city_1} - {self.city_2} ({self.date_begin} - {self.date_end})'

    class Meta:
        verbose_name = 'Тариф OI'
        verbose_name_plural = 'Тарифы OI'


class Subclass(models.Model):
    name_code = models.CharField(max_length=255, verbose_name='Код')
    name_description = models.CharField(max_length=255, verbose_name='Описание')
    created_by = models.CharField(max_length=10, verbose_name='Логин, кем создана запись')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_by = models.CharField(max_length=10, verbose_name='Логин, вносивший изменение')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name_code

    class Meta:
        verbose_name = 'Вид почты'
        verbose_name_plural = 'Виды почты'


class Commission(models.Model):
    gpa = models.ForeignKey(GPACode, on_delete=models.CASCADE, verbose_name='Связанный GPA')
    value = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Значение')
    created_by = models.CharField(max_length=10, verbose_name='Логин, кем создана запись')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_by = models.CharField(max_length=10, verbose_name='Логин, вносивший изменение')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'Комиссия для GPA {self.gpa} - {self.value}%'

    class Meta:
        verbose_name = 'Комиссия'
        verbose_name_plural = 'Комиссии'


class ExchangeRate(models.Model):
    rate_1 = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange_rate_1', verbose_name='Валюта 1')
    rate_2 = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange_rate_2', verbose_name='Валюта 2')
    value = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Значение')
    created_by = models.CharField(max_length=10, verbose_name='Логин, кем создана запись')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_by = models.CharField(max_length=10, verbose_name='Логин, вносивший изменение')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'Обменный курс {self.rate_1} к {self.rate_2} - {self.value}'

    class Meta:
        verbose_name = 'Обменный курс'
        verbose_name_plural = 'Обменные курсы'

