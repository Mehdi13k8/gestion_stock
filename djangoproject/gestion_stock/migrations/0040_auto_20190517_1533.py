# Generated by Django 2.1.7 on 2019-05-17 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_stock', '0039_auto_20190517_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imgaccueil',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
