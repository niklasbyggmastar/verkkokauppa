# Generated by Django 2.0.2 on 2018-08-28 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0053_auto_20180828_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]