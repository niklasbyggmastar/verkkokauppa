# Generated by Django 2.0.2 on 2018-07-23 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0013_profile_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='ad_1',
        ),
        migrations.RemoveField(
            model_name='category',
            name='ad_2',
        ),
    ]
