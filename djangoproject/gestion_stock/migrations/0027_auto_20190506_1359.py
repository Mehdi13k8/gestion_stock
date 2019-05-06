# Generated by Django 2.1.7 on 2019-05-06 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_stock', '0026_auto_20190506_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonlivraisonentree_pour_lettrevoiturelettrevoitureentree',
            name='fk_BonLivraisonEntree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_stock.BonLivraisonEntree'),
        ),
        migrations.AlterField(
            model_name='bonlivraisonentree_pour_lettrevoiturelettrevoitureentree',
            name='fk_LettreVoitureEntree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_stock.LettreVoitureEntree'),
        ),
        migrations.AlterField(
            model_name='lettrevoitureentree',
            name='fk_Transporteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_stock.Transporteur'),
        ),
    ]
