# Generated by Django 2.0.2 on 2018-08-06 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0031_auto_20180806_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='age',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='email',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='gender',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='nickname',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
