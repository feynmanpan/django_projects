# Generated by Django 3.0.3 on 2020-03-03 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0112_bookprice_url_ebook'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinfo',
            name='bookid_ebook',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='bookinfo',
            name='price_sale_ebook',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
