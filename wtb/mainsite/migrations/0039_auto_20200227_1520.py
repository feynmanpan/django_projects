# Generated by Django 3.0.3 on 2020-02-27 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0038_auto_20200227_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='url',
            field=models.URLField(blank=True, default='', null=True),
        ),
    ]