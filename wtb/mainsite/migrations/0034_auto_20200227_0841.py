# Generated by Django 3.0.3 on 2020-02-27 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0033_bookinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='isbn',
            field=models.CharField(default='9789571234567', max_length=13),
        ),
    ]
