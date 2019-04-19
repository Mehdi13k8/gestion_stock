# Generated by Django 2.1.7 on 2019-04-17 10:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexible', '0003_auto_20190408_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date_from', models.DateField(default=datetime.date.today, verbose_name='date from')),
                ('date_to', models.DateField(default=datetime.date.today, verbose_name='date to')),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
