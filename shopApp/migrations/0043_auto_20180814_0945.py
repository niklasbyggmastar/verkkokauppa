# Generated by Django 2.0.2 on 2018-08-14 06:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0042_auto_20180812_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='my_lists',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0, unique=True), blank=True, default=[], size=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='shopping_cart',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0, unique=True), blank=True, default=[], size=50),
        ),
    ]
