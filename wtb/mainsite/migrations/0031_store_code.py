# Generated by Django 3.0.3 on 2020-02-21 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0030_auto_20200221_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='code',
            field=models.CharField(default='00', max_length=2),
        ),
    ]