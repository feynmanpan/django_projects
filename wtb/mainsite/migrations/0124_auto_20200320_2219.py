# Generated by Django 3.0.3 on 2020-03-20 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0123_bookprice_stock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinfo',
            options={'ordering': ('-create_dt',)},
        ),
    ]
