# Generated by Django 3.0.3 on 2020-03-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0121_bookinfo_url_vdo'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookprice',
            name='url_vdo',
            field=models.URLField(blank=True, default=''),
        ),
    ]
