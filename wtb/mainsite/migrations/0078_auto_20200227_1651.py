# Generated by Django 3.0.3 on 2020-02-27 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0077_auto_20200227_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='url',
            field=models.URLField(blank=True, default=None),
        ),
    ]
