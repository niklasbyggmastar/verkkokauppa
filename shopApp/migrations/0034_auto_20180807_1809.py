# Generated by Django 2.0.2 on 2018-08-07 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0033_auto_20180807_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='age',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='gender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='nickname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]