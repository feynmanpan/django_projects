# Generated by Django 3.0.3 on 2020-02-19 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0006_auto_20200219_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='url_href',
            field=models.CharField(default='', max_length=200),
        ),
    ]