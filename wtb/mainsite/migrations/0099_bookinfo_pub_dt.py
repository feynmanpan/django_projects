# Generated by Django 3.0.3 on 2020-02-28 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0098_auto_20200227_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinfo',
            name='pub_dt',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='出版日期'),
        ),
    ]