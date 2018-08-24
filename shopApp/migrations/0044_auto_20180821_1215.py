# Generated by Django 2.0.2 on 2018-08-21 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0043_auto_20180814_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='street_address',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='zip_code',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]