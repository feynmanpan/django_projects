# Generated by Django 3.0.3 on 2020-03-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0124_auto_20200320_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookprice',
            name='url_book',
            field=models.URLField(blank=True, default='', max_length=600),
        ),
        migrations.AlterField(
            model_name='bookprice',
            name='url_ebook',
            field=models.URLField(blank=True, default='', max_length=600),
        ),
    ]
