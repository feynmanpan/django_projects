# Generated by Django 3.0.3 on 2020-03-03 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0111_bookprice_price_sale_ebook'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookprice',
            name='url_ebook',
            field=models.URLField(blank=True, default=''),
        ),
    ]
