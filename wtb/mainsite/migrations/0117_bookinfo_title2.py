# Generated by Django 3.0.3 on 2020-03-11 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0116_bookinfo_spec'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinfo',
            name='title2',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
