# Generated by Django 3.0.3 on 2020-02-27 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0095_auto_20200227_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='err',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
