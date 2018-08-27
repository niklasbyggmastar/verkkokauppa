# Generated by Django 2.0.2 on 2018-08-27 14:06

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0048_auto_20180827_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_num',
            field=phonenumber_field.modelfields.PhoneNumberField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='street_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='zip_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
