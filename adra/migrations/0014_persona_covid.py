# Generated by Django 3.0.5 on 2020-07-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adra', '0013_auto_20200711_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='covid',
            field=models.BooleanField(default=False, verbose_name='Entregas pandemia'),
        ),
    ]
