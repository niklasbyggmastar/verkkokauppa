# Generated by Django 2.0.2 on 2018-08-27 14:45

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0050_auto_20180827_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_num',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True),
        ),
    ]