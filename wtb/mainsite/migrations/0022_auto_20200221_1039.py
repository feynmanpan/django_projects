# Generated by Django 3.0.3 on 2020-02-21 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0021_auto_20200221_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='url_href',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]