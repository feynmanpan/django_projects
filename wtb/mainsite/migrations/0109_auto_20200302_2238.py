# Generated by Django 3.0.3 on 2020-03-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0108_bookprice_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='code',
            field=models.CharField(default='999', max_length=3),
        ),
    ]
