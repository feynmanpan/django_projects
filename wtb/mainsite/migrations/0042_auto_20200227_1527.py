# Generated by Django 3.0.3 on 2020-02-27 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0041_auto_20200227_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
