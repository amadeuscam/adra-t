# Generated by Django 2.1.2 on 2020-06-27 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adra', '0011_add_email_validators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='mensaje',
            field=models.TextField(blank=True),
        ),
    ]
