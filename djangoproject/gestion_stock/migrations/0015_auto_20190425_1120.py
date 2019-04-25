# Generated by Django 2.1.7 on 2019-04-25 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_stock', '0014_auto_20190425_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bonlivraisonentree',
            name='fk_LettreVoitureEntree',
        ),
        migrations.RemoveField(
            model_name='bonlivraisonentree_pour_boncommandeentree',
            name='fk_BonCommandeEntree',
        ),
        migrations.RemoveField(
            model_name='bonlivraisonentree_pour_boncommandeentree',
            name='fk_LettreVoitureEntree',
        ),
        migrations.AlterField(
            model_name='bonlivraisonentree_pour_boncommandeentree',
            name='fk_Destinataire_litige',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gestion_stock.Destinataire'),
        ),
        migrations.AlterField(
            model_name='bonlivraisonentree_pour_boncommandeentree',
            name='fk_Fournisseur',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_stock.Fournisseur'),
        ),
    ]
