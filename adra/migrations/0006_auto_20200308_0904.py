# Generated by Django 2.1.2 on 2020-03-08 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adra', '0005_remove_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
