# Generated by Django 2.1.7 on 2019-05-28 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_stock', '0046_auto_20190528_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='colis',
            name='colle',
            field=models.CharField(default='Null', max_length=42),
        ),
    ]
