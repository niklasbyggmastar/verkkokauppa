# Generated by Django 2.0.2 on 2018-06-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0003_item_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(default='', max_length=200),
        ),
    ]
