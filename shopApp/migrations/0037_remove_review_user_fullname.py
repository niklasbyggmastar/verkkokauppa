# Generated by Django 2.0.2 on 2018-08-10 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0036_review_user_fullname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user_fullname',
        ),
    ]
