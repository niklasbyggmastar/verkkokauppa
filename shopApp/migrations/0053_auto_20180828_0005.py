# Generated by Django 2.0.2 on 2018-08-27 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0052_auto_20180827_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
