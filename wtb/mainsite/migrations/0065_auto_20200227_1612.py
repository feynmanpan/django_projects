# Generated by Django 3.0.3 on 2020-02-27 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0064_auto_20200227_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='err',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]