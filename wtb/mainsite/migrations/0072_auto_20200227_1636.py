# Generated by Django 3.0.3 on 2020-02-27 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0071_auto_20200227_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='err',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
