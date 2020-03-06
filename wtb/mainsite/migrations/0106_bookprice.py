# Generated by Django 3.0.3 on 2020-03-02 01:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0105_auto_20200228_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookprice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('err', models.CharField(blank=True, default='', max_length=50)),
                ('store', models.CharField(blank=True, default='', max_length=10)),
                ('price_sale', models.CharField(blank=True, default='', max_length=10)),
                ('create_dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新日期')),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.Bookinfo')),
            ],
            options={
                'ordering': ('bookid',),
            },
        ),
    ]