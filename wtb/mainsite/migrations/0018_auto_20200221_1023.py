# Generated by Django 3.0.3 on 2020-02-21 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0017_auto_20200221_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='url',
            field=models.URLField(blank=True, default=None),
        ),
    ]