# Generated by Django 3.0.3 on 2020-02-27 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0091_auto_20200227_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='err',
            field=models.CharField(blank=True, default='@Q', max_length=100),
        ),
    ]
