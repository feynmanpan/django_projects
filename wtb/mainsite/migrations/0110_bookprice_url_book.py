# Generated by Django 3.0.3 on 2020-03-03 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0109_auto_20200302_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookprice',
            name='url_book',
            field=models.URLField(blank=True, default=''),
        ),
    ]
