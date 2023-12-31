# Generated by Django 4.2.4 on 2023-11-16 17:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_module", "0008_report_alter_kzdrate_created_by_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Records",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("GPACode", models.CharField(max_length=255)),
                ("Origin", models.CharField(max_length=255)),
                ("Destination", models.CharField(max_length=255)),
                ("Subclass", models.CharField(max_length=255)),
                ("Flight1", models.CharField(max_length=255)),
                ("FltDate", models.CharField(max_length=10)),
                ("Wgt", models.FloatField()),
                ("Depeche", models.CharField(max_length=255)),
                ("GroupDate", models.CharField(max_length=10)),
                (
                    "created_by",
                    models.CharField(
                        max_length=10, verbose_name="Логин, кем создана запись"
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "modified_by",
                    models.CharField(
                        max_length=10, verbose_name="Логин, вносивший изменение"
                    ),
                ),
                (
                    "modified_date",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Report",
        ),
    ]
