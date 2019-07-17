import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
from django import forms
# Create your models here.

'''class User(models.Model):
    users = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_partenaire = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_transporteur = models.BooleanField(default=False)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)'''

#Models for Import_Bon_CommandeSortie
'''class import_BonCommandeSortie(models.Model):
    idBonCommandeSortie = models.TextField(default=0)
    Client = models.TextField(default=0)
    Destinataire2 = models.TextField(default=0)
    Destinataire = models.TextField(default=0)
    codeDestinataire = models.TextField(default=0)
    Transporteur = models.TextField(default=0)
    numeroCommande = models.TextField(default=0)
    dateCommande = models.TextField(default=0)
    source = models.TextField(default=0)
    def __str__(self):
        return self.idBonCommandeSortie

class import_LigneBonCommandeSortie_pour_import_BonCommandeSortie(models.Model):
    idLigneBonCommandeSortie = models.TextField(default=0)
    fk_BonCommandeSortie = models.ForeignKey('import_BonCommandeSortie', on_delete=models.SET_NULL, default=0)
    Article = models.TextField(default=0)
    designation = models.TextField(default=0)
    quantiteProduitCommande = models.TextField(default=0)
    priorite = models.TextField(default=0)
    source = models.TextField(default=0)
    idArticle_CDK = models.TextField(default=0)
    quantiteColisStandard_CDK = models.TextField(default=0)
    def __str__(self):
        return self.idLigneBonCommandeSortie'''#je n'en ai plus besoin car via la view je rempli directement la tab LigneBonCommandeSortie_pour_BonCommandeSortie

'''class UniteManutentionSortie_pour_BonCommandeSortie(models.Model):
    idUniteManutentionSortie = models.TextField()
    fk_TypeUniteManutentionSortie = models.ForeignKey('TypeUniteManutention_pour_UniteManutentionSortie', on_delete=models.SET_NULL, default=0)
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_import_BonCommandeSortie', on_delete=models.SET_NULL, default=0)
    #fk_BonLivraisonSortie = models.ForeignKey('', on_delete=models.SET_NULL, default=0)
    fk_Etiquette = models.ForeignKey('EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=0)
    numero = models.TextField()
    dateOuverture = models.TextField()
    dateExpedition = models.TextField()
    dateFermeture = models.TextField()
    poidsBrut = models.TextField()
    poidsTare = models.TextField()
    poidsNet = models.TextField()
    poidsDifference = models.TextField()
    stat_poidsBrut = models.TextField()'''

'''class TypeUniteManutention_pour_UniteManutentionSortie(models.Model):
    idTypeUniteManutention = models.TextField()
    nom = models.TextField()'''

'''class BonCommandeSortie_pour_import_BonCommandeSortie(models.Model):
    #idBonCommandeSortie = models.CharField(max_length=150)
    idBonCommandeSortie = models.TextField()#db_index=True)
    c_nom = models.TextField()#db_index=True)
    c_nomCompte = models.TextField()#db_index=True)
    c_horodatage = models.TextField()#db_index=True)
    m_nom = models.TextField()#db_index=True)
    m_nomCompte = models.TextField()#db_index=True)
    m_horodatage = models.TextField()#db_index=True)
    fk_Client = models.ForeignKey('Client_pour_import_BonCommandeSortie', on_delete=models.SET_NULL, related_name='clients',default=0)
    fk_Destinataire = models.ForeignKey('Destinataire_pour_import_BonCommandeSortie', on_delete=models.SET_NULL, default=0)
    fk_Transporteur = models.ForeignKey('Transporteur_pour_import_BonCommandeSortie', on_delete=models.SET_NULL, default=0)
    fk_TypeBonCommandeSortie = models.ForeignKey('TypeBonCommandeSortie_pour_BonCommandeSortie', on_delete=models.SET_NULL, default=0)
    numeroCommande = models.TextField(default=0)
    dateCommande = models.TextField(default=0)
    termine = models.TextField(default=0)
    source = models.TextField(default=0)
    identifiantSource = models.TextField(default=0)
    def __str__(self):
        return self.idBonCommandeSortie'''

class LigneBonCommandeSortie_pour_BonCommandeSortie(models.Model):
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idLigneBonCommandeSortie = models.CharField(max_length=150, default=0)
    quantiteProduitCommande = models.CharField(max_length=150, default=0)
    quantiteColisCommande  = models.CharField(max_length=150, default=0)
    quantiteProduitALivrer = models.CharField(max_length=150, default=0)
    quantiteProduitLivre = models.CharField(max_length=150, default=0)
    quantiteColisLivre = models.CharField(max_length=150, default=0)
    quantiteProduitPotentielle = models.CharField(max_length=150, default=0)
    quantiteColisPotentielle = models.CharField(max_length=150, default=0)
    differenceCommandeLivre = models.CharField(max_length=150, default=0)
    differenceCommandePotentiel = models.CharField(max_length=150, default=0)
    priorite = models.CharField(max_length=150, default=0)
    termine = models.CharField(max_length=150, default=0)
    priorite = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idLigneBonCommandeSortie

'''class Article_pour_BonCommandeSortie(models.Model):
    idArticle = models.CharField(max_length=150)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.SET_NULL, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.SET_NULL, default=0)
    codeFournisseur = models.CharField(max_length=150, default=0)
    codeClient = models.CharField(max_length=150, default=0)
    designationFournisseur = models.CharField(max_length=150, default=0)
    designationClient = models.CharField(max_length=150, default=0)
    dureeStockage = models.CharField(max_length=150, default=0)
    delaiPeremption = models.CharField(max_length=150, default=0)
    stock = models.CharField(max_length=150, default=0)
    poidsColisStandard = models.CharField(max_length=150, default=0)
    quantiteColisStandard = models.CharField(max_length=150, default=0)
    quantiteColisStockComplet = models.CharField(max_length=150, default=0)
    quantiteProduitStockComplet = models.CharField(max_length=150, default=0)
    quantiteColisStockIncomplet = models.CharField(max_length=150, default=0)
    quantiteProduitStockIncomplet = models.CharField(max_length=150, default=0)
    quantiteUniteManutentionSortie = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idArticle'''

'''class Client_pour_import_BonCommandeSortie(models.Model):
    idClient = models.CharField(max_length=150)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    fk_TypeZone = models.ForeignKey('TypeZoneDepot', on_delete=models.SET_NULL, default=0)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.SET_NULL, default=0)
    fk_Destinataire = models.ForeignKey('Destinataire_pour_import_BonCommandeSortie', on_delete=models.SET_NULL, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.SET_NULL, default=0)
    nom = models.CharField(max_length=150, default=0)
    adresse = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    siret = models.CharField(max_length=150, default=0)
    tva = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    nomCompte = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idClient'''

'''class Destinataire_pour_import_BonCommandeSortie(models.Model):
    idDestinataire = models.CharField(max_length=150, default=0)
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_BonCommandeSortie', on_delete=models.SET_NULL, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    adresseLivraison = models.CharField(max_length=150, default=0)
    adresseFacturation = models.CharField(max_length=150, default=0)
    departement = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    identifiantBonLivraison = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    codeUM = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    adresseLivraison_nom = models.CharField(max_length=150, default=0)
    adresseLivraison_numero = models.CharField(max_length=150, default=0)
    adresseLivraison_rue = models.CharField(max_length=150, default=0)
    adresseLivraison_complement_1 = models.CharField(max_length=150, default=0)
    adresseLivraison_complement_2 = models.CharField(max_length=150, default=0)
    adresseLivraison_codePostal = models.CharField(max_length=150, default=0)
    adresseLivraison_localite = models.CharField(max_length=150, default=0)
    fk_Pays = models.ForeignKey('Pays_pour_Destinataire', on_delete=models.SET_NULL, default=0)
    delaiPeremption = models.CharField(max_length=150, default=0)
    ordreTri = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class TypeDestinataire_pour_BonCommandeSortie(models.Model):
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idTypeDestinataire = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class Transporteur_pour_import_BonCommandeSortie(models.Model):
    idTransporteur = models.CharField(max_length=150, default='0')
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class BonLivraisonSortie_pour_BonCommandeSortie(models.Model):
    idBonLivraisonSortie = models.CharField(max_length=150, default='0')
    c_horodatage = models.CharField(max_length=150, default='0')
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_import_BonCommandeSortie', on_delete=models.SET_NULL, default=0)
    numeroBonLivraison = models.CharField(max_length=150, default='0')'''

#End of Import_BonCommandeSortie

#Models for BonCommandeEntree
class BonCommandeEntree(models.Model):
    idBonCommandeEntree = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    numeroCommande = models.CharField(max_length=150, default=0)
    dateCommande = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    #fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, default=0)
    #fk_Client = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL)
    def __str__(self):
        return self.idBonCommandeEntree

class LigneBonCommandeEntree_pour_BonCommandeEntree(models.Model):
    idLigneBonCommandeEntree = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    dateLivraison = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    quantiteColis = models.CharField(max_length=150, default=0)
    quantiteProduit = models.CharField(max_length=150, default=0)
    quantiteRecue = models.CharField(max_length=150, default=0)
    fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_BonCommandeEntree = models.ForeignKey('BonCommandeEntree', on_delete=models.SET_NULL, default=0, blank=True, null=True)

'''class Article_pour_BonCommandeEntree(models.Model):
    idArticle = models.CharField(max_length=150, default=0)
    fk_BonCommandeEntree = models.ForeignKey('BonCommandeEntree', on_delete=models.SET_NULL, default=0)
    fk_Fournisseur = models.ForeignKey('Fournisseur_pour_Article', on_delete=models.SET_NULL, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.SET_NULL, default=0)
    codeClient = models.CharField(max_length=150, default=0)
    designationFournisseur = models.CharField(max_length=150, default=0)
    designationClient = models.CharField(max_length=150, default=0)
    dureeStockage = models.CharField(max_length=150, default=0)
    delaiPeremption = models.CharField(max_length=150, default=0)
    stock = models.CharField(max_length=150, default=0)
    poidsColisStandard = models.CharField(max_length=150, default=0)
    quantiteColisStandard = models.CharField(max_length=150, default=0)
    quantiteColisStockComplet = models.CharField(max_length=150, default=0)
    quantiteProduitStockComplet = models.CharField(max_length=150, default=0)
    quantiteColisStockIncomplet = models.CharField(max_length=150, default=0)
    quantiteProduitStockInComplet = models.CharField(max_length=150, default=0)
    quantiteUniteManutentionSortie = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idArticle'''

'''class BonCommandeEntree_BonLivraisonEntree_pour_BonCommandeEntree(models.Model):
    idBonCommandeEntree_BonLivraisonEntree = models.CharField(max_length=150, default=0)
    fk_BonCommandeEntree = models.ForeignKey('BonCommandeEntree', on_delete=models.SET_NULL, default=0)
    fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree_pour_BonCommandeEntree', on_delete=models.SET_NULL, default=0)
    source = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idArticle'''

'''class BonLivraisonEntree_pour_BonCommandeEntree(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=150, default=0)
    #fk_BonCommandeEntree = models.ForeignKey('BonCommandeEntree', on_delete=models.SET_NULL, default=0)
    #fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.SET_NULL, default=0)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Client = models.ForeignKey('Client', on_delete=models.SET_NULL, default=0)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Destinataire_litige = models.ForeignKey('Destinataire', on_delete=models.SET_NULL, default=0)
    #fk_ZoneDepot_litige = models.ForeignKey('Destinataire_pour_UniteManutentionEntree_litige', on_delete=models.SET_NULL, default=0)
    fichier = models.CharField(max_length=150, default=0)
    photo = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idBonLivraisonEntree'''

'''class UniteManutentionEntree_pour_BonCommandeEntree(models.Model):
    id_BonCommandeEntree = models.CharField(max_length=150, default=0)
    id_dateReception = models.CharField(max_length=150, default=0)
    #fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree_pour_BonCommandeEntree', on_delete=models.SET_NULL, default=0)
    def __str__(self):
        return self.id_BonCommandeEntree'''

'''class Colis_pour_BonCommandeEntree(models.Model):
    idColis = models.CharField(max_length=150, default=0)
    #fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.SET_NULL, default=0)
    #fk_UniteManutentionSortie = models.ForeignKey('UniteManutentionSortie', on_delete=models.SET_NULL, default=0)
    #fk_EtiquetteColis = models.ForeignKey('', on_delete=models.SET_NULL, default=0)
    #fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree_pour_BonCommandeEntree', on_delete=models.SET_NULL, default=0)'''

'''class LigneBonLivraisonEntree_pour_BonCommandeEntree(models.Model):
    idLigneBonLivraisonEntree = models.CharField(max_length=150, default=0)
    fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree', on_delete=models.SET_NULL, default=0)
    fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0)
    controle = models.CharField(max_length=150, default=0)
    quantiteColis = models.CharField(max_length=150, default=0)
    quantiteColisAlivrer = models.CharField(max_length=150, default=0)
    quantiteColisLitige = models.CharField(max_length=150, default=0)
    quantiteColisRecu = models.CharField(max_length=150, default=0)
    quantiteCommande = models.CharField(max_length=150, default=0)
    quantiteCommandeRecue = models.CharField(max_length=150, default=0)
    quantiteDifference = models.CharField(max_length=150, default=0)
    quantiteDifferenceAutre = models.CharField(max_length=150, default=0)
    quantiteDifferenceRestante = models.CharField(max_length=150, default=0)
    quantiteProduit = models.CharField(max_length=150, default=0)
    quantiteProduitALivrer = models.CharField(max_length=150, default=0)
    quantiteProduitLitige = models.CharField(max_length=150, default=0)
    quantiteProduitRecu = models.CharField(max_length=150, default=0)
    quantiteRecue = models.CharField(max_length=150, default=0)
    termine = models.CharField(max_length=150, default=0)'''

#End of BonCommandeEntree

#Models for LettreVoitureEntree
class LettreVoitureEntree(models.Model):
    idLettreVoitureEntree = models.CharField(max_length=150, default=0)
    datereception = models.CharField(max_length=150, default=0)
    numerorecepisse = models.CharField(max_length=150, default=0)
    quantitepalette = models.CharField(max_length=150, default=0)
    quantitecolis = models.CharField(max_length=150, default=0)
    reclaquantitepalette = models.CharField(max_length=150, default=0)
    reclaquantitecolis = models.CharField(max_length=150, default=0)
    reclacomm = models.CharField(max_length=150, default=0)
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.SET_NULL, null=True, blank=True)
    fichier = models.ImageField(upload_to='media_lve/', default=None, blank=True, null=True)
    photo = models.ImageField(upload_to='media_lve/', default=None, blank=True, null=True)
    def __str__(self):
        return self.idLettreVoitureEntree

'''class BonLivraisonEntree_pour_LettreVoitureLettreVoitureEntree(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=150, default=0)
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.SET_NULL, null=True, blank=True)
    fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.idBonLivraisonEntree'''

'''class Client_pour_LettreVoitureEntree(models.Model):
    idClient = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idClient'''

'''class OrdreTransport_pour_LettreVoitureEntree(models.Model):
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.SET_NULL, default=0)'''

'''class Transporteur_pour_LettreVoitureEntree(models.Model):
    idTransporteur = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idTransporteur'''

#End of LettreVoitureEntree

class LettreVoitureSortie(models.Model):
    idLettreVoitureSortie = models.CharField(max_length=150, default=0)
    datereception = models.CharField(max_length=150, default=0)
    numerorecepisse = models.CharField(max_length=150, default=0)
    quantitepalette = models.CharField(max_length=150, default=0)
    quantitecolis = models.CharField(max_length=150, default=0)
    reclaquantitepalette = models.CharField(max_length=150, default=0)
    reclaquantitecolis = models.CharField(max_length=150, default=0)
    reclacomm = models.CharField(max_length=150, default=0)
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.idLettreVoitureSortie

class Transporteur(models.Model):
    idTransporteur = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

#article
class Article(models.Model):
    idArticle = models.CharField(max_length=150, default=0)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    #fk_Fournisseur = models.ForeignKey('Fournisseur_pour_Article', on_delete=models.SET_NULL, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    codeFournisseur = models.CharField(max_length=150, default='0')
    codeClient = models.CharField(max_length=150, default='0')
    designationFournisseur = models.CharField(max_length=150, default='0')
    designationClient = models.CharField(max_length=150, default='0')
    dureeStockage = models.CharField(max_length=150, default='0')
    delaiPeremption = models.CharField(max_length=150, default='0')
    stock = models.CharField(max_length=150, default='0')
    poidsColisStandard = models.CharField(max_length=150, default='0')
    quantiteColisStandard = models.CharField(max_length=150, default='0')
    quantiteColisStockComplet = models.CharField(max_length=150, default='0')
    quantiteProduitStockComplet = models.CharField(max_length=150, default='0')
    quantiteColisStockIncomplet = models.CharField(max_length=150, default='0')
    quantiteProduitStockIncomplet = models.CharField(max_length=150, default='0')
    quantiteUniteManutentionSortie = models.CharField(max_length=150, default='0')
    source = models.CharField(max_length=150, default='0')
    identifiantSource = models.CharField(max_length=150, default='0')
    def __str__(self):
        return self.designationClient

'''class Colis_pour_Article(models.Model):
    fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idColis = models.CharField(max_length=150, default=0)
    fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.SET_NULL, default=0)
    """fk_UniteManutentionSortie = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0)
    fk_EtiquetteColis = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0)
    fk_ColisStandard = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0)
    fk_litige = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0)
    fk_litigeDecision = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0)
    fk_Colis = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0)"""
    #fk_ZoneDepot = models.ForeignKey('ZoneDepot_pour_UniteManutentionEntree_colis', on_delete=models.SET_NULL, default=0)
    emplacementConfirme = models.CharField(max_length=150, default=0)
    numeroLot = models.CharField(max_length=150, default=0)
    datePeremption = models.CharField(max_length=150, default=0)
    quantiteProduit = models.CharField(max_length=150, default=0)
    numerotation = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idColis'''

class Article_historique_pour_Article(models.Model):
    fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    #fk_Fournisseur = models.ForeignKey('Fournisseur_pour_Article_historique', on_delete=models.SET_NULL, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idArticle_historique = models.CharField(max_length=150, default=0)
    nomFournisseur = models.CharField(max_length=150, default=0)
    codeFournisseur = models.CharField(max_length=150, default=0)
    designationFournisseur = models.CharField(max_length=150, default=0)
    codeClient = models.CharField(max_length=150, default=0)
    designationClient = models.CharField(max_length=150, default=0)
    poids = models.CharField(max_length=150, default=0)
    delaiPeremption = models.CharField(max_length=150, default=0)
    dureeStockage = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idArticle_historique

'''class Fournisseur_pour_Article_historique(models.Model):
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    #fk_type = models.ForeignKey('#', on_delete=models.SET_NULL, default=0)
    idFournisseur = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class Article_Destinataire_pour_Article(models.Model):
    fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0)
    fk_Destinataire = models.ForeignKey('Destinataire_pour_Article', on_delete=models.SET_NULL, default=0)
    idArticle_Destinataire = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    delaiPeremption = models.CharField(max_length=150, default=0)
    #Rubrique11 = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idArticle_Destinataire'''

'''class Destinataire_pour_Article(models.Model):
    idDestinataire = models.CharField(max_length=150, default=0)
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.SET_NULL, default=0)
    #fk_BonLivraisonEntree = models.ForeignKey('client_pour_import_boncommandesortie', on_delete=models.SET_NULL, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    adresseLivraison = models.CharField(max_length=150, default=0)
    adresseFacturation = models.CharField(max_length=150, default=0)
    departement = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    identifiantBonLivraison = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    codeUM = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    adresseLivraison_nom = models.CharField(max_length=150, default=0)
    adresseLivraison_numero = models.CharField(max_length=150, default=0)
    adresseLivraison_rue = models.CharField(max_length=150, default=0)
    adresseLivraison_complement_1 = models.CharField(max_length=150, default=0)
    adresseLivraison_complement_2 = models.CharField(max_length=150, default=0)
    adresseLivraison_codePostal = models.CharField(max_length=150, default=0)
    adresseLivraison_localite = models.CharField(max_length=150, default=0)
    fk_Pays = models.ForeignKey('Pays_pour_Destinataire', on_delete=models.SET_NULL, default=0)
    delaiPeremption = models.CharField(max_length=150, default=0)
    ordreTri = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class Client_pour_Article_typeDestinataire(models.Model):
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.SET_NULL, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idClient = models.CharField(max_length=150, default=0)
    fk_TypeZone = models.ForeignKey('TypeZoneDepot', on_delete=models.SET_NULL, default=0)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.SET_NULL, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.SET_NULL, default=0)
    nom = models.CharField(max_length=150, default=0)
    adress = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    siret = models.CharField(max_length=150, default=0)
    tva = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    nomCompte = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class Fournisseur_pour_Article(models.Model):
    idFournisseur = models.CharField(max_length=150, default=0)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.SET_NULL, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class Client_pour_Article_typeArticle(models.Model):
    fk_TypeZone = models.ForeignKey('TypeZoneDepot', on_delete=models.SET_NULL, default=0)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.SET_NULL, default=0)
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.SET_NULL, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.SET_NULL, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idClient = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    adress = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    siret = models.CharField(max_length=150, default=0)
    tva = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    nomCompte = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

class typeArticle_pour_Article(models.Model):
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idTypeArticle = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

#endof article

#Destinataire
class Destinataire(models.Model):
    idDestinataire = models.CharField(max_length=150, default=0)
    fk_Pays = models.ForeignKey('Pays_pour_Destinataire', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    adresseLivraison = models.CharField(max_length=150, default=0)
    adresseFacturation = models.CharField(max_length=150, default=0)
    departement = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    identifiantBonLivraison = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    codeUM = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    adresseLivraison_nom = models.CharField(max_length=150, default=0)
    adresseLivraison_numero = models.CharField(max_length=150, default=0)
    adresseLivraison_rue = models.CharField(max_length=150, default=0)
    adresseLivraison_complement_1 = models.CharField(max_length=150, default=0)
    adresseLivraison_complement_2 = models.CharField(max_length=150, default=0)
    adresseLivraison_codePostal = models.CharField(max_length=150, default=0)
    adresseLivraison_localite = models.CharField(max_length=150, default=0)
    delaiPeremption = models.CharField(max_length=150, default=0)
    ordreTri = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

'''class BonCommandeSortie_pour_Destinataire(models.Model):
    idBonCommandeSortie = models.CharField(max_length=150, default=0)
    fk_Destinataire = models.ForeignKey('Destinataire', on_delete=models.SET_NULL, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    #fk_Client = models.ForeignKey('Destinataire', on_delete=models.SET_NULL, default=0)
    #fk_Destinataire = models.ForeignKey('Destinataire', on_delete=models.SET_NULL, default=0)
    #fk_Transporteur = models.ForeignKey('Destinataire', on_delete=models.SET_NULL, default=0)
    #fk_TypeBonCommandeSortie = models.ForeignKey('Destinataire', on_delete=models.SET_NULL, default=0)
    numeroCommande = models.CharField(max_length=150, default=0)
    dateCommande = models.CharField(max_length=150, default=0)
    termine = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.numeroCommande'''

'''class UniteManutentionSortie_pour_Destinataire(models.Model):
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_Destinataire', on_delete=models.SET_NULL, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idUniteManutentionSortie = models.CharField(max_length=150, default=0)
    #fk_TypeUniteManutention = models.ForeignKey('', on_delete=models.SET_NULL, default=0)
    #fk_BonLivraisonSortie = models.ForeignKey('', on_delete=models.SET_NULL, default=0)
    #fk_Etiquette = models.ForeignKey('', on_delete=models.SET_NULL, default=0)
    numero = models.CharField(max_length=150, default=0)
    dateOuverture = models.CharField(max_length=150, default=0)
    dateFermeture = models.CharField(max_length=150, default=0)
    dateExpedition = models.CharField(max_length=150, default=0)
    poidsBrut = models.CharField(max_length=150, default=0)
    poidsTare = models.CharField(max_length=150, default=0)
    poidsNet = models.CharField(max_length=150, default=0)
    poidsDifference = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.numero'''

class TypeDestinataire_pour_Destinataire(models.Model):
    idTypeDestinataire = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

class Pays_pour_Destinataire(models.Model):
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idPays = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    codeISO_2 = models.CharField(max_length=150, default=0)
    codeISO_3 = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom
    #endof destinataire

#Start Client

class Client(models.Model):
    idClient = models.CharField(max_length=150, default=0)
    fk_TypeZone = models.ForeignKey('TypeZoneDepot', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    adresse = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    siret = models.CharField(max_length=150, default=0)
    tva = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    nomCompte = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

'''class BonCommandeSortie_pour_Client(models.Model):
    fk_Client = models.ForeignKey('Client', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idBonCommandeSortie = models.CharField(max_length=150, default=0)
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.SET_NULL, default=1)
    fk_TypeBonCommandeSortie = models.ForeignKey('TypeBonCommandeSortie_pour_BonCommandeSortie', on_delete=models.SET_NULL, default=1)
    fk_Destinataire = models.ForeignKey('Destinataire', on_delete=models.SET_NULL, default=1)
    numeroCommande = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idBonCommandeSortie

class BonLivraisonEntree_pour_Client(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=150, default=0)
    fk_Client = models.ForeignKey('Client', on_delete=models.SET_NULL, default=1)
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.SET_NULL, default=1)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, default=1)
    #fk_Destinataire_litige = models.ForeignKey('Destinataire_pour_BonLivraisonEntree', on_delete=models.SET_NULL, default=1)
    #fk_ZoneDepot_litige = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, default=1)
    dateReception = models.CharField(max_length=150, default=0)
    numeroBonLivraison = models.CharField(max_length=150, default=0)
    quantitePalette = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)

class OrdreTransport_pour_Client(models.Model):
    idOrdreTransport = models.CharField(max_length=150, default=0)
    fk_Client = models.ForeignKey('Client', on_delete=models.SET_NULL, default=1)
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.SET_NULL, default=1)
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    dateCreation = models.CharField(max_length=150, default=0)
    '''

class Contact_pour_Client(models.Model):
    idContact = models.CharField(max_length=150, default=0)
    fk_Client = models.ForeignKey('Client', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_RoleContact = models.ForeignKey('RoleContact_pour_Client', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    prenom = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

class RoleContact_pour_Client(models.Model):
    idRoleContact = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

'''class TypeZoneDepot_pour_Client(models.Model):
    idTypeZoneDepot = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)

class TypeFournisseur_pour_Client(models.Model):
    idTypeFournisseur = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)

class TypeDestinataire_pour_Client(models.Model):
    idTypeFournisseur = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)

class TypeArticle_pour_Client(models.Model):
    idTypeArticle = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    '''

#end of Client

#ressource
class TypeZoneDepot(models.Model):
    idTypeZoneDepot = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

class ZoneDepot_pour_TypeZoneDepot(models.Model):
    #fk_TypeZoneDepot = models.ForeignKey('TypeZoneDepot', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_TypeZoneDepot = models.ForeignKey('TypeZoneDepot', on_delete=models.SET_NULL, default=None, blank=True, null=True)
    idZoneDepot = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

class TypeFournisseur_pour_Fournisseur(models.Model):
    idTypeFournisseur = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

class Fournisseur(models.Model):
    idFournisseur = models.CharField(max_length=150, default=0)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

class TypeBonCommandeSortie_pour_BonCommandeSortie(models.Model): #pas utilisé !
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idTypeBonCommandeSortie = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

#Unitemanutentionentree debut

class UniteManutentionEntree(models.Model):
    idUniteManutentionEntree = models.CharField(max_length=150, default=0)
    fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_ZoneDepot = models.ForeignKey('ZoneDepot_pour_TypeZoneDepot', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    #fk_Etiquette = models.ForeignKey('EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    numero = models.CharField(max_length=150, default=0)
    dateReception = models.CharField(max_length=150, default=0)
    stock = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idUniteManutentionEntree

'''class Colis_pour_UniteManutentionEntree(models.Model):
    idColis = models.CharField(max_length=150, default=0)
    #fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    fk_UniteManutentionSortie = models.ForeignKey('UniteManutentionSortie_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    fk_EtiquetteColis = models.ForeignKey('EtiquetteColis_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    fk_Article = models.ForeignKey('Article_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    fk_litige = models.ForeignKey('Litige_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    fk_LitigeDecision = models.ForeignKey('LitigeDecision_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    #fk_ZoneDepot = models.ForeignKey('ZoneDepot_pour_UniteManutentionEntree_colis', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    #fk_Colis = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    #fk_ColisStandard = models.ForeignKey('', on_delete=models.SET_NULL, default=1)
    emplacementConfirme = models.CharField(max_length=150, default=0)
    numeroLot = models.CharField(max_length=150, default=0)
    datePeremption = models.CharField(max_length=150, default=0)
    quantiteProduit = models.CharField(max_length=150, default=0)
    numerotation = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idColis'''

'''class EtiquetteColis_pour_UniteManutentionEntree_historique(models.Model):
    fk_Colis = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idEtiquetteColis = models.CharField(max_length=150, default=0)
    expediteur = models.CharField(max_length=150, default=0)
    codeArticleFournisseur = models.CharField(max_length=150, default=0)
    nomCompte = models.CharField(max_length=150, default=0)
    quantiteProduit = models.CharField(max_length=150, default=0)
    numeroLot = models.CharField(max_length=150, default=0)
    datePeremption = models.CharField(max_length=150, default=0)
    designationArticleFournisseur = models.CharField(max_length=150, default=0)
    codeUM = models.CharField(max_length=150, default=0)
    Fournisseur = models.CharField(max_length=150, default=0)
    datamatrix_humaine = models.CharField(max_length=150, default=0)
    retour = models.CharField(max_length=150, default=0)
    collee = models.CharField(max_length=150, default=0)
    afficherExpediteur = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class Colis_ZoneDepot_pour_UniteManutentionEntree(models.Model):
    fk_Colis = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idColis_ZoneDepot = models.CharField(max_length=150, default=0)
    fk_ZoneDepot = models.ForeignKey('ZoneDepot_pour_UniteManutentionEntree_colis', on_delete=models.SET_NULL, default=1)
    dateEntree = models.CharField(max_length=150, default=0)
    dateSortie = models.CharField(max_length=150, default=0)'''
    #def __str__(self):
    #return self.nom

'''class Colis_UniteManutentionSortie_pour_UniteManutentionEntree(models.Model):
    fk_Colis = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    fk_UniteManutentionSortie = models.ForeignKey('UniteManutentionSortie_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    idColis_UniteManutentionSortie = models.CharField(max_length=150, default=0)'''

'''class UniteManutentionSortie_pour_UniteManutentionEntree(models.Model):
    idColis = models.CharField(max_length=150, default=0)
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)'''

'''class BonCommandeSortie_pour_UniteManutentionEntree(models.Model):
    idBonCommandeSortie = models.CharField(max_length=150, default=0)
    fk_Destinataire = models.ForeignKey('Destinataire_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    fk_TypeBonCommandeSortie = models.ForeignKey('TypeBonCommandeSortie_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)'''

'''class Destinataire_pour_UniteManutentionEntree(models.Model):
    idDestinataire = models.CharField(max_length=150, default=0)'''

'''class TypeBonCommandeSortie_pour_UniteManutentionEntree(models.Model):
    idTypeBonCommandeSortie = models.CharField(max_length=150, default=0)'''

'''class EtiquetteColis_pour_UniteManutentionEntree(models.Model):
    idEtiquetteColis = models.CharField(max_length=150, default=0)'''

'''class Article_pour_UniteManutentionEntree(models.Model):
    idArticle = models.CharField(max_length=150, default=0)
    fk_Fournisseur = models.ForeignKey('Fournisseur_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    fk_TypeFournisseur = models.ForeignKey('TypeArticle_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)'''

'''class Fournisseur_pour_UniteManutentionEntree(models.Model):
    idFournisseur = models.CharField(max_length=150, default=0)'''

'''class TypeArticle_pour_UniteManutentionEntree(models.Model):
    idTypeArticle = models.CharField(max_length=150, default=0)'''

'''class Litige_pour_UniteManutentionEntree(models.Model):
    idLitige = models.CharField(max_length=150, default=0)'''

'''class LitigeDecision_pour_UniteManutentionEntree(models.Model):
    idLitigeDecision = models.CharField(max_length=150, default=0)'''

'''class ZoneDepot_pour_UniteManutentionEntree_colis(models.Model):
    idZoneDepot = models.CharField(max_length=150, default=0)
    fk_TypeZoneDepot = models.ForeignKey('TypeZoneDepot_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class LotRetire_pour_UniteManutentionEntree_pour_UniteManutentionEntree_historique(models.Model):
    fk_Article = models.ForeignKey('UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    numeroLot = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    idLotRetire = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idLotRetire'''

'''class EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree_historique(models.Model):
    fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idEtiquetteUniteManutentionEntree = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idEtiquetteUniteManutentionEntree'''

'''class BonLivraisonEntree_pour_UniteManutentionEntree(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=150, default=0)
    fk_Client = models.ForeignKey('Client_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    fk_Destinataire_litige = models.ForeignKey('Destinataire_pour_UniteManutentionEntree_litige', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    #fk_LettreVoitureEntree = models.ForeignKey('', on_delete=models.SET_NULL, default=1)
    #fk_Fournisseur = models.ForeignKey('', on_delete=models.SET_NULL, default=1)
    #fk_ZoneDepot_litige = models.ForeignKey('', on_delete=models.SET_NULL, default=1)
    dateReception = models.CharField(max_length=150, default=0)
    numeroBonLivraison = models.CharField(max_length=150, default=0)
    quantitePalette = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idBonLivraisonEntree'''

'''class Client_pour_UniteManutentionEntree(models.Model):
    idClient = models.CharField(max_length=150, default=0)
    fk_TypeZone = models.ForeignKey('TypeZoneDepot_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    #fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.SET_NULL, default=1)
    #fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.SET_NULL, default=1)
    #fk_TypeArticle = models.ForeignKey('TypeArticle_pour_Article', on_delete=models.SET_NULL, default=1)
    nom = models.CharField(max_length=150, default=0)
    adresse = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    siret = models.CharField(max_length=150, default=0)
    tva = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    nomCompte = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class Destinataire_pour_UniteManutentionEntree_litige(models.Model):
    idDestinataire = models.CharField(max_length=150, default=0)
    #fk_TypeDestinataire = models.ForeignKey('', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    adresseLivraison = models.CharField(max_length=150, default=0)
    adresseFacturation = models.CharField(max_length=150, default=0)
    departement = models.CharField(max_length=150, default=0)
    telephone = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    identifiantBonLivraison = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    codeUM = models.CharField(max_length=150, default=0)
    email = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    adresseLivraison_nom = models.CharField(max_length=150, default=0)
    adresseLivraison_numero = models.CharField(max_length=150, default=0)
    adresseLivraison_rue = models.CharField(max_length=150, default=0)
    adresseLivraison_complement_1 = models.CharField(max_length=150, default=0)
    adresseLivraison_complement_2 = models.CharField(max_length=150, default=0)
    adresseLivraison_codePostal = models.CharField(max_length=150, default=0)
    adresseLivraison_localite = models.CharField(max_length=150, default=0)
    fk_Pays = models.ForeignKey('Pays_pour_Destinataire', on_delete=models.SET_NULL, default=1)
    delaiPeremption = models.CharField(max_length=150, default=0)
    ordreTri = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class TypeZoneDepot_pour_UniteManutentionEntree(models.Model):
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    idTypeZoneDepot = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class ZoneDepot_pour_UniteManutentionEntree(models.Model):
    idZoneDepot = models.CharField(max_length=150, default=0)
    #fk_TypeZoneDepot = models.ForeignKey('', on_delete=models.SET_NULL, default=1)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom'''

'''class EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree(models.Model):
    #fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    idEtiquetteUniteManutentionEntree = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    client = models.CharField(max_length=150, default=0)
    numeroUM = models.CharField(max_length=150, default=0)
    zone = models.CharField(max_length=150, default=0)
    fournisseur = models.CharField(max_length=150, default=0)
    quantiteColis = models.CharField(max_length=150, default=0)
    dateReception = models.CharField(max_length=150, default=0)
    nomCompte = models.CharField(max_length=150, default=0)
    collee = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nomCompte'''
#fin

#début Colis
class Colis(models.Model):
    idColis = models.CharField(max_length=150, default=0)
    fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.CASCADE    , default=0, blank=True, null=True)
    fk_UniteManutentionSortie = models.ForeignKey('UniteManutentionSortie', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    #fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    #Article_pour_Colisfk_Article= models.ForeignKey('Article', on_delete=models.SET_NULL, default=1)
    fk_litige  = models.ForeignKey('Litige', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_LitigeDecision = models.ForeignKey('LitigeDecision', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    numeroLot = models.CharField(max_length=150, default=0)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    #fk_EtiquetteColis= models.ForeignKey('', on_delete=models.SET_NULL, default=1)
    #fk_ColisStandard = models.ForeignKey('', on_delete=models.SET_NULL, default=1)
    fk_ZoneDepot = models.ForeignKey('ZoneDepot_pour_TypeZoneDepot', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    emplacementConfirme = models.CharField(max_length=150, default=0)
    datePeremption = models.CharField(max_length=150, default=0)
    quantiteProduit = models.CharField(max_length=150, default=0)
    colle = models.CharField(max_length=150, default=0)
    numerotation = models.CharField(max_length=150, default=0)
    def __str__(self):
        if self.fk_UniteManutentionSortie != None:
            return str("colis " + self.idColis + " expedié UMs : " + self.fk_UniteManutentionSortie.idUniteManutentionSortie)
        else:
            return str("colis " + self.idColis)

class Litige(models.Model):
    idLitige = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

class LitigeDecision(models.Model):
    idLitige = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.nom

'''class LotRetire_pour_Colis(models.Model):
    fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=1)
    dateRetrait = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    idLotRetire = models.CharField(max_length=150, default=0)
    numeroLot = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)'''

'''class Colis_UniteManutentionSortie_pour_Colis(models.Model):
    idColis_UniteManutentionSortie = models.CharField(max_length=150, default=0)'''

'''class UniteManutentionEntree_pour_Colis(models.Model):
    idUniteManutentionEntree = models.CharField(max_length=150, default=0)'''

'''class UniteManutentionSortie_pour_Colis(models.Model):
    idUniteManutentionSortie = models.CharField(max_length=150, default=0)'''

'''class Article_pour_Colis(models.Model):
    idArticle = models.CharField(max_length=150, default=0)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, default=1)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.SET_NULL, default=1)
    codeFournisseur = models.CharField(max_length=150, default=0)
    codeClient = models.CharField(max_length=150, default=0)
    designationFournisseur = models.CharField(max_length=150, default=0)
    designationClient = models.CharField(max_length=150, default=0)
    dureeStockage = models.CharField(max_length=150, default=0)
    delaiPeremption = models.CharField(max_length=150, default=0)
    stock = models.CharField(max_length=150, default=0)
    poidsColisStandard = models.CharField(max_length=150, default=0)
    quantiteColisStandard = models.CharField(max_length=150, default=0)
    quantiteColisStockComplet = models.CharField(max_length=150, default=0)
    quantiteProduitStockComplet = models.CharField(max_length=150, default=0)
    quantiteColisStockIncomplet = models.CharField(max_length=150, default=0)
    quantiteProduitStockincomplet = models.CharField(max_length=150, default=0)
    quantiteUniteManutentionSortie = models.CharField(max_length=150, default=0)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)'''


#fin
#début Bon Livraison Sortie

class BonLivraisonSortie(models.Model):
    idBonLivraisonSortie = models.CharField(max_length=150, default=0)
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_LettreVoitureSortie = models.ForeignKey('LettreVoitureSortie', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    dateImpression = models.CharField(max_length=150, default=0)
    numeroBonLivraison = models.CharField(max_length=150, default=0)
    prixExpedition = models.CharField(max_length=150, default=0)
    codeTracking = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    #fk_Transporteur = models.ForeignKey('', on_delete=models.SET_NULL, default=1)

'''class UniteManutentionSortie_pour_BonLivraisonSortie(models.Model):
    idUniteManutentionSortie = models.CharField(max_length=150, default=0)
    fk_BonLivraisonSortie = models.ForeignKey('Colis_pour_BonLivraisonSortie', on_delete=models.SET_NULL, default=1)
    numero = models.CharField(max_length=150, default=0)'''

'''class Colis_pour_BonLivraisonSortie(models.Model):
    idColis = models.CharField(max_length=150, default=0)
    #fk_UniteManutentionSortie = models.ForeignKey('UniteManutentionSortie_pour_BonLivraisonSortie', on_delete=models.SET_NULL, default=1)
    fk_Article = models.ForeignKey('Article_pour_BonLivraisonSortie_Colis', on_delete=models.SET_NULL, default=1)'''

'''class Article_pour_BonLivraisonSortie_Colis(models.Model):
    idArticle = models.CharField(max_length=150, default=0)'''

class LigneBonLivraisonSortie_pour_BonLivraisonSortie(models.Model):
    idLigneBonLivraisonSortie = models.CharField(max_length=150, default=0)
    fk_BonLivraisonSortie = models.ForeignKey('BonLivraisonSortie', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Article = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    quantiteColis = models.CharField(max_length=150, default=0)
    stat_quantiteColis = models.CharField(max_length=150, default=0)

'''class Article_pour_BonLivraisonSortie(models.Model):
    idArticle = models.CharField(max_length=150, default=0)'''

'''class BonCommandeSortie_pour_BonLivraisonSortie(models.Model):
    idBonCommandeSortie = models.CharField(max_length=150, default=0)
    fk_Client = models.ForeignKey('Client_pour_BonLivraisonSortie', on_delete=models.SET_NULL, default=1)
    fk_Destinataire = models.ForeignKey('Destinataire_pour_BonLivraisonSortie', on_delete=models.SET_NULL, default=1)'''

'''class LigneBonCommandeSortie_pour_BonLivraisonSortie(models.Model):
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_BonLivraisonSortie', on_delete=models.SET_NULL, default=1)
    idLigneBonCommandeSortie = models.CharField(max_length=150, default=0)'''

'''class Client_pour_BonLivraisonSortie(models.Model):
    idClient = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)'''

'''class Destinataire_pour_BonLivraisonSortie(models.Model):
    idDestinataire = models.CharField(max_length=150, default=0)
    nom = models.CharField(max_length=150, default=0)
    identifiantBonLivraison = models.CharField(max_length=150, default=0)
    codeUM = models.CharField(max_length=150, default=0)'''

'''class LettreVoitureSortie_pour_BonLivraisonSortie(models.Model):
    idLettreVoitureSortie = models.CharField(max_length=150, default=0)
    numeroRecepisse = models.CharField(max_length=150, default=0)'''

class BonCommandeSortie(models.Model):
    idBonCommandeSortie = models.CharField(max_length=150, default=0)
    termine = models.CharField(max_length=150, default=0)
    fichier = models.ImageField(upload_to='media_bcs/', default=None, blank=True, null=True)
    source = models.CharField(max_length=150, default=0)
    identifiantSource = models.CharField(max_length=150, default=0)
    numeroCommande = models.CharField(max_length=150, default=0)
    dateCommande = models.CharField(max_length=150, default=0)
    fk_Client = models.ForeignKey('Client', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Destinataire = models.ForeignKey('Destinataire', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    #fk_TypeBonCommandeSortie = models.ForeignKey('TypeBonCommandeSortie_pour_BonCommandeSortie', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    def __str__(self):
        return self.numeroCommande

class BonLivraisonEntree(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=150, default=0)
    fk_LettreVoitureEntree  = models.ForeignKey('LettreVoitureEntree', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_TypeZoneDepot = models.ForeignKey('TypeZoneDepot', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_ZoneDepot_pour_TypeZoneDepot = models.ForeignKey('ZoneDepot_pour_TypeZoneDepot', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    #fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    #fk_BonCommandeEntree = models.ForeignKey('BonCommandeEntree', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Client = models.ForeignKey('Client', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Destinataire = models.ForeignKey('Destinataire', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    dateReception = models.CharField(max_length=150, default=0)
    numeroBonLivraison = models.CharField(max_length=150, default=0)
    quantitePalette = models.CharField(max_length=150, default=0)
    commentaire = models.CharField(max_length=150, default=0)
    fichier = models.ImageField(upload_to='media_ble/', default=None, blank=True, null=True)
    photo = models.ImageField(upload_to='media_ble/', default=None, blank=True, null=True)
    def __str__(self):
        return self.idBonLivraisonEntree

class LigneBonLivraisonEntree_pour_BonLivraisonEntree(models.Model):
    idLigneBonLivraisonEntree = models.CharField(max_length=150, default=0)
    fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_Article  = models.ForeignKey('Article', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    controle = models.CharField(max_length=150, default=0)
    quantiteColis = models.CharField(max_length=150, default=0)
    quantiteColisAlivrer = models.CharField(max_length=150, default=0)
    quantiteColisLitige = models.CharField(max_length=150, default=0)
    quantiteColisRecu = models.CharField(max_length=150, default=0)
    quantiteCommande = models.CharField(max_length=150, default=0)
    quantiteCommandeRecue = models.CharField(max_length=150, default=0)
    quantiteDifference = models.CharField(max_length=150, default=0)
    quantiteDifferenceAutre = models.CharField(max_length=150, default=0)
    quantiteDifferenceRestante = models.CharField(max_length=150, default=0)
    quantiteProduit = models.CharField(max_length=150, default=0)
    quantiteProduitAlivrer = models.CharField(max_length=150, default=0)
    quantiteProduitLitige = models.CharField(max_length=150, default=0)
    quantiteProduitRecu = models.CharField(max_length=150, default=0)
    termine = models.CharField(max_length=150, default=0)

'''class imgaccueil(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.title

class imgumentree(models.Model):
    photo = models.ImageField(upload_to='imgumentree')

class imgarticle(models.Model):
    photo = models.ImageField(upload_to='imgarticle')

class imgclient(models.Model):
    photo = models.ImageField(upload_to='imgclient')

class imgbcs(models.Model):
    photo = models.ImageField(upload_to='imgbcs')

class imgdestinataires(models.Model):
    photo = models.ImageField(upload_to='imgdestinataires')

class imgtransporteurs(models.Model):
    photo = models.ImageField(upload_to='imgtransporteurs')

class imgbls(models.Model):
    photo = models.ImageField(upload_to='imgbls')

class imgfournisseurs(models.Model):
    photo = models.ImageField(upload_to='imgfournisseurs')

class imgble(models.Model):
    photo = models.ImageField(upload_to='imgble')

class imgcolis(models.Model):
    photo = models.ImageField(upload_to='imgcolis')

class imglve(models.Model):
    photo = models.ImageField(upload_to='imglve')
'''

class menuimages(models.Model):
    title = models.TextField()
    cover1 = models.ImageField(upload_to='images/', blank=True)
    cover2 = models.ImageField(upload_to='images/', blank=True)
    cover3 = models.ImageField(upload_to='images/', blank=True)
    cover4 = models.ImageField(upload_to='images/', blank=True)
    cover5 = models.ImageField(upload_to='images/', blank=True)
    cover6 = models.ImageField(upload_to='images/', blank=True)
    cover7 = models.ImageField(upload_to='images/', blank=True)
    cover8 = models.ImageField(upload_to='images/', blank=True)
    cover9 = models.ImageField(upload_to='images/', blank=True)
    cover10 = models.ImageField(upload_to='images/', blank=True)
    cover11 = models.ImageField(upload_to='images/', blank=True)
    cover12 = models.ImageField(upload_to='images/', blank=True)
    cover13 = models.ImageField(upload_to='images/', blank=True)
    cover14 = models.ImageField(upload_to='images/', blank=True)
    def __str__(self):
        return self.title

class UniteManutentionSortie(models.Model):
    idUniteManutentionSortie = models.CharField(max_length=150, default=0)
    #fk_UniteManutentionEntre = models.ForeignKey('UniteManutentionEntree', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    #fk_Etiquette = models.ForeignKey('EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree', on_delete=models.SET_NULL, default=1)
    #fk_TypeUniteManutention_pour_UniteManutentionSortie = models.ForeignKey('TypeUniteManutention_pour_UniteManutentionSortie', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie', on_delete=models.CASCADE, default=0, blank=True, null=True)
    fk_BonLivraisonSortie = models.ForeignKey('BonLivraisonSortie', on_delete=models.SET_NULL, default=0, blank=True, null=True)
    c_nom = models.CharField(max_length=150, default=0)
    c_nomCompte = models.CharField(max_length=150, default=0)
    c_horodatage = models.CharField(max_length=150, default=0)
    m_nom = models.CharField(max_length=150, default=0)
    m_nomCompte = models.CharField(max_length=150, default=0)
    m_horodatage = models.CharField(max_length=150, default=0)
    numero = models.CharField(max_length=150, default=0)
    dateReception = models.CharField(max_length=150, default=0)
    dateExpedition = models.CharField(max_length=150, default=0)
    dateOuverture = models.CharField(max_length=150, default=0)
    poidsBrut = models.CharField(max_length=150, default=0)
    poidsDifference = models.CharField(max_length=150, default=0)
    poidsNet = models.CharField(max_length=150, default=0)
    poidsTare = models.CharField(max_length=150, default=0)
    def __str__(self):
        return self.idUniteManutentionSortie
