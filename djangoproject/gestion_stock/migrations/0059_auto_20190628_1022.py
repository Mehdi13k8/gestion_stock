# Generated by Django 2.1.7 on 2019-06-28 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_stock', '0058_auto_20190626_0913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unitemanutentionentree',
            name='fk_ZoneDepot',
        ),
        migrations.AlterField(
            model_name='zonedepot_pour_typezonedepot',
            name='fk_TypeZoneDepot',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_stock.TypeZoneDepot'),
        ),
    ]
