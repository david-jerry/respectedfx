# Generated by Django 4.2.6 on 2023-10-16 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fxrates", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="exchangerates",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
