# Generated by Django 3.0.3 on 2020-03-14 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0119_bookprice_isbn13'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinfo',
            name='intro',
            field=models.TextField(blank=True, default='', max_length=3000),
        ),
    ]