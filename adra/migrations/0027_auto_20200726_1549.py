# Generated by Django 2.1.2 on 2020-07-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adra', '0026_hijo_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_pics'),
        ),
    ]
