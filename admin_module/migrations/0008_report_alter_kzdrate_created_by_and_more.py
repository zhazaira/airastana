# Generated by Django 4.2.4 on 2023-11-16 13:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_module", "0007_remove_kzdrate_rate_eli"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
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
                ("FltDate", models.DateField()),
                ("Wgt", models.FloatField()),
                ("Depeche", models.CharField(max_length=255)),
                ("GroupDate", models.DateField()),
                ("CREATED_BY", models.CharField(max_length=255)),
                ("CREATED_DATE", models.DateField(auto_now_add=True)),
                ("MODIFIED_BY", models.CharField(max_length=255)),
                ("MODIFIED_DATE", models.DateField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name="kzdrate",
            name="created_by",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="Логин, кем создана запись"
            ),
        ),
        migrations.AlterField(
            model_name="kzdrate",
            name="modified_by",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="Логин, вносивший изменение"
            ),
        ),
        migrations.AlterField(
            model_name="oirate",
            name="created_by",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="Логин, кем создана запись"
            ),
        ),
        migrations.AlterField(
            model_name="oirate",
            name="modified_by",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="Логин, вносивший изменение"
            ),
        ),
        migrations.AlterField(
            model_name="sdrrate",
            name="created_by",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="Логин, кем создана запись"
            ),
        ),
        migrations.AlterField(
            model_name="sdrrate",
            name="modified_by",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="Логин, вносивший изменение"
            ),
        ),
    ]