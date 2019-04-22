import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class User(models.Model):
    users = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_partenaire = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_transporteur = models.BooleanField(default=False)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)

#Models for Import_Bon_CommandeSortie
class import_BonCommandeSortie(models.Model):
    idBonCommandeSortie = models.TextField(default='Null')
    Client = models.TextField(default='Null')
    Destinataire2 = models.TextField(default='Null')    
    Destinataire = models.TextField(default='Null')
    codeDestinataire = models.TextField(default='Null')
    Transporteur = models.TextField(default='Null')
    numeroCommande = models.TextField(default='Null')
    dateCommande = models.TextField(default='Null')
    source = models.TextField(default='Null')
    def __str__(self):
        return self.idBonCommandeSortie

class import_LigneBonCommandeSortie_pour_import_BonCommandeSortie(models.Model):
    idLigneBonCommandeSortie = models.TextField(default='Null')
    fk_BonCommandeSortie = models.ForeignKey('import_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    Article = models.TextField(default='Null')
    designation = models.TextField(default='Null')
    quantiteProduitCommande = models.TextField(default='Null')
    priorite = models.TextField(default='Null')
    source = models.TextField(default='Null')
    idArticle_CDK = models.TextField(default='Null')
    quantiteColisStandard_CDK = models.TextField(default='Null')
    
    def __str__(self):
        return self.idLigneBonCommandeSortie

class UniteManutentionSortie_pour_BonCommandeSortie(models.Model):
    idUniteManutentionSortie = models.TextField()
    fk_TypeUniteManutentionSortie = models.ForeignKey('TypeUniteManutention_pour_UniteManutentionSortie', on_delete=models.CASCADE, default=0)
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_import_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    #fk_BonLivraisonSortie = models.ForeignKey('', on_delete=models.CASCADE, default=0)
    fk_Etiquette = models.ForeignKey('EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=0)
    numero = models.TextField()
    dateOuverture = models.TextField()
    dateExpedition = models.TextField()
    dateFermeture = models.TextField()
    poidsBrut = models.TextField()
    poidsTare = models.TextField()
    poidsNet = models.TextField()
    poidsDifference = models.TextField()
    stat_poidsBrut = models.TextField()

class TypeUniteManutention_pour_UniteManutentionSortie(models.Model):
    idTypeUniteManutention = models.TextField()
    nom = models.TextField()

class BonCommandeSortie_pour_import_BonCommandeSortie(models.Model):
    #idBonCommandeSortie = models.CharField(max_length=42)
    idBonCommandeSortie = models.TextField()#db_index=True)
    c_nom = models.TextField()#db_index=True)
    c_nomCompte = models.TextField()#db_index=True)
    c_horodatage = models.TextField()#db_index=True)
    m_nom = models.TextField()#db_index=True)
    m_nomCompte = models.TextField()#db_index=True)
    m_horodatage = models.TextField()#db_index=True)
    fk_Client = models.ForeignKey('Client_pour_import_BonCommandeSortie', on_delete=models.CASCADE, related_name='clients',default=0)
    fk_Destinataire = models.ForeignKey('Destinataire_pour_import_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    fk_Transporteur = models.ForeignKey('Transporteur_pour_import_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    fk_TypeBonCommandeSortie = models.ForeignKey('TypeBonCommandeSortie_pour_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    numeroCommande = models.TextField(default='Null')
    dateCommande = models.TextField(default='Null')
    termine = models.TextField(default='Null')
    source = models.TextField(default='Null')
    identifiantSource = models.TextField(default='Null')
    def __str__(self):
        return self.idBonCommandeSortie

class LigneBonCommandeSortie_pour_import_BonCommandeSortie(models.Model):
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_import_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    fk_Article = models.ForeignKey('Article_pour_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idLigneBonCommandeSortie = models.CharField(max_length=42, default='Null')
    quantiteProduitCommande = models.CharField(max_length=42, default='Null')
    quantiteColisCommande  = models.CharField(max_length=42, default='Null')
    quantiteProduitALivrer = models.CharField(max_length=42, default='Null')
    quantiteProduitLivre = models.CharField(max_length=42, default='Null')
    quantiteColisLivre = models.CharField(max_length=42, default='Null')
    quantiteProduitPotentielle = models.CharField(max_length=42, default='Null')
    quantiteColisPotentielle = models.CharField(max_length=42, default='Null')
    differenceCommandeLivre = models.CharField(max_length=42, default='Null')
    differenceCommandePotentiel = models.CharField(max_length=42, default='Null')
    priorite = models.CharField(max_length=42, default='Null')
    termine = models.CharField(max_length=42, default='Null')
    priorite = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idLigneBonCommandeSortie

class Article_pour_BonCommandeSortie(models.Model):
    idArticle = models.CharField(max_length=42)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.CASCADE, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.CASCADE, default=0)
    codeFournisseur = models.CharField(max_length=42, default='Null')
    codeClient = models.CharField(max_length=42, default='Null')
    designationFournisseur = models.CharField(max_length=42, default='Null')
    designationClient = models.CharField(max_length=42, default='Null')
    dureeStockage = models.CharField(max_length=42, default='Null')
    delaiPeremption = models.CharField(max_length=42, default='Null')
    stock = models.CharField(max_length=42, default='Null')
    poidsColisStandard = models.CharField(max_length=42, default='Null')
    quantiteColisStandard = models.CharField(max_length=42, default='Null')
    quantiteColisStockComplet = models.CharField(max_length=42, default='Null')
    quantiteProduitStockComplet = models.CharField(max_length=42, default='Null')
    quantiteColisStockIncomplet = models.CharField(max_length=42, default='Null')
    quantiteProduitStockIncomplet = models.CharField(max_length=42, default='Null')
    quantiteUniteManutentionSortie = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idArticle

class Client_pour_import_BonCommandeSortie(models.Model):
    idClient = models.CharField(max_length=42)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    fk_TypeZone = models.ForeignKey('TypeZoneDepot', on_delete=models.CASCADE, default=0)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.CASCADE, default=0)
    fk_Destinataire = models.ForeignKey('Destinataire_pour_import_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.CASCADE, default=0)
    nom = models.CharField(max_length=42, default='Null')
    adresse = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    telephone = models.CharField(max_length=42, default='Null')
    email = models.CharField(max_length=42, default='Null')
    siret = models.CharField(max_length=42, default='Null')
    tva = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    nomCompte = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idClient

class Destinataire_pour_import_BonCommandeSortie(models.Model):
    idDestinataire = models.CharField(max_length=42, default=0)
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default=0)
    c_nomCompte = models.CharField(max_length=42, default=0)
    c_horodatage = models.CharField(max_length=42, default=0)
    m_nom = models.CharField(max_length=42, default=0)
    m_nomCompte = models.CharField(max_length=42, default=0)
    m_horodatage = models.CharField(max_length=42, default=0)
    adresseLivraison = models.CharField(max_length=42, default=0)
    adresseFacturation = models.CharField(max_length=42, default=0)
    departement = models.CharField(max_length=42, default=0)
    telephone = models.CharField(max_length=42, default=0)
    nom = models.CharField(max_length=42, default=0)
    identifiantBonLivraison = models.CharField(max_length=42, default=0)
    commentaire = models.CharField(max_length=42, default=0)
    codeUM = models.CharField(max_length=42, default=0)
    email = models.CharField(max_length=42, default=0)
    source = models.CharField(max_length=42, default=0)
    identifiantSource = models.CharField(max_length=42, default=0)
    adresseLivraison_nom = models.CharField(max_length=42, default=0)
    adresseLivraison_numero = models.CharField(max_length=42, default=0)
    adresseLivraison_rue = models.CharField(max_length=42, default=0)
    adresseLivraison_complement_1 = models.CharField(max_length=42, default=0)
    adresseLivraison_complement_2 = models.CharField(max_length=42, default=0)
    adresseLivraison_codePostal = models.CharField(max_length=42, default=0)
    adresseLivraison_localite = models.CharField(max_length=42, default=0)
    fk_Pays = models.ForeignKey('Pays_pour_Destinataire', on_delete=models.CASCADE, default=0)
    delaiPeremption = models.CharField(max_length=42, default=0)
    ordreTri = models.CharField(max_length=42, default=0)
    def __str__(self):
        return self.nom

class TypeDestinataire_pour_BonCommandeSortie(models.Model):
    c_nom = models.CharField(max_length=42, default=0)
    c_nomCompte = models.CharField(max_length=42, default=0)
    c_horodatage = models.CharField(max_length=42, default=0)
    m_nom = models.CharField(max_length=42, default=0)
    m_nomCompte = models.CharField(max_length=42, default=0)
    m_horodatage = models.CharField(max_length=42, default=0)
    idTypeDestinataire = models.CharField(max_length=42, default=0)
    nom = models.CharField(max_length=42, default=0)
    def __str__(self):
        return self.nom

class Transporteur_pour_import_BonCommandeSortie(models.Model):
    idTransporteur = models.CharField(max_length=42, default='0')
    c_nom = models.CharField(max_length=42, default=0)
    c_nomCompte = models.CharField(max_length=42, default=0)
    c_horodatage = models.CharField(max_length=42, default=0)
    m_nom = models.CharField(max_length=42, default=0)
    m_nomCompte = models.CharField(max_length=42, default=0)
    m_horodatage = models.CharField(max_length=42, default=0)
    nom = models.CharField(max_length=42, default=0)
    def __str__(self):
        return self.nom

class BonLivraisonSortie_pour_BonCommandeSortie(models.Model):
    idBonLivraisonSortie = models.CharField(max_length=42, default='0')
    c_horodatage = models.CharField(max_length=42, default='0')
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_import_BonCommandeSortie', on_delete=models.CASCADE, default=0)
    numeroBonLivraison = models.CharField(max_length=42, default='0')

#End of Import_BonCommandeSortie

#Models for BonCommandeEntree
class BonCommandeEntree(models.Model):
    idBonCommandeEntree = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    numeroCommande = models.CharField(max_length=42, default='Null')
    dateCommande = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    #fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, default=0)
    #fk_Client = models.ForeignKey('Fournisseur', on_delete=models.CASCADE)
    def __str__(self):
        return self.idBonCommandeEntree

class LigneBonCommandeEntree_pour_BonCommandeEntree(models.Model):
    idLigneBonCommandeEntree = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    dateLivraison = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    quantiteColis = models.CharField(max_length=42, default='Null')
    quantiteProduit = models.CharField(max_length=42, default='Null')
    quantiteRecue = models.CharField(max_length=42, default='Null')
    fk_Article = models.ForeignKey('Article_pour_BonCommandeEntree', on_delete=models.CASCADE, default=0)
    fk_BonCommandeEntree = models.ForeignKey('BonCommandeEntree', on_delete=models.CASCADE, default=0)

class Article_pour_BonCommandeEntree(models.Model):
    idArticle = models.CharField(max_length=42, default='Null')
    fk_BonCommandeEntree = models.ForeignKey('BonCommandeEntree', on_delete=models.CASCADE, default=0)
    fk_Fournisseur = models.ForeignKey('Fournisseur_pour_Article', on_delete=models.CASCADE, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.CASCADE, default=0)
    codeClient = models.CharField(max_length=42, default='Null')
    designationFournisseur = models.CharField(max_length=42, default='Null')
    designationClient = models.CharField(max_length=42, default='Null')
    dureeStockage = models.CharField(max_length=42, default='Null')
    delaiPeremption = models.CharField(max_length=42, default='Null')
    stock = models.CharField(max_length=42, default='Null')
    poidsColisStandard = models.CharField(max_length=42, default='Null')
    quantiteColisStandard = models.CharField(max_length=42, default='Null')
    quantiteColisStockComplet = models.CharField(max_length=42, default='Null')
    quantiteProduitStockComplet = models.CharField(max_length=42, default='Null')
    quantiteColisStockIncomplet = models.CharField(max_length=42, default='Null')
    quantiteProduitStockInComplet = models.CharField(max_length=42, default='Null')
    quantiteUniteManutentionSortie = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idArticle

class BonCommandeEntree_BonLivraisonEntree_pour_BonCommandeEntree(models.Model):
    idBonCommandeEntree_BonLivraisonEntree = models.CharField(max_length=42, default='Null')
    fk_BonCommandeEntree = models.ForeignKey('BonCommandeEntree', on_delete=models.CASCADE, default=0)
    fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree_pour_BonCommandeEntree', on_delete=models.CASCADE, default=0)
    source = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idArticle

class BonLivraisonEntree_pour_BonCommandeEntree(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=42, default='Null')
    fk_BonCommandeEntree = models.ForeignKey('BonCommandeEntree', on_delete=models.CASCADE, default=0)
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.CASCADE, default=0)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, default=0)
    fk_Client = models.ForeignKey('Client', on_delete=models.CASCADE, default=0)
    fk_Destinataire_litige = models.ForeignKey('Destinataire_pour_UniteManutentionEntree_litige', on_delete=models.CASCADE, default=0)
    #fk_ZoneDepot_litige = models.ForeignKey('Destinataire_pour_UniteManutentionEntree_litige', on_delete=models.CASCADE, default=0)
    fichier = models.CharField(max_length=42, default='Null')
    photo = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idBonLivraisonEntree

class UniteManutentionEntree_pour_BonCommandeEntree(models.Model):
    id_BonCommandeEntree = models.CharField(max_length=42, default='Null')
    id_dateReception = models.CharField(max_length=42, default='Null')
    #fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree_pour_BonCommandeEntree', on_delete=models.CASCADE, default=0)
    def __str__(self):
        return self.id_BonCommandeEntree

class Colis_pour_BonCommandeEntree(models.Model):
    idColis = models.CharField(max_length=42, default='Null')
    #fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.CASCADE, default=0)
    #fk_UniteManutentionSortie = models.ForeignKey('UniteManutentionSortie', on_delete=models.CASCADE, default=0)
    #fk_EtiquetteColis = models.ForeignKey('', on_delete=models.CASCADE, default=0)
    #fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree_pour_BonCommandeEntree', on_delete=models.CASCADE, default=0)

class LigneBonLivraisonEntree_pour_BonCommandeEntree(models.Model):
    idLigneBonLivraisonEntree = models.CharField(max_length=42, default='Null')
    fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree', on_delete=models.CASCADE, default=0)
    fk_Article = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)
    controle = models.CharField(max_length=42, default='Null')
    quantiteColis = models.CharField(max_length=42, default='Null')
    quantiteColisAlivrer = models.CharField(max_length=42, default='Null')
    quantiteColisLitige = models.CharField(max_length=42, default='Null')
    quantiteColisRecu = models.CharField(max_length=42, default='Null')
    quantiteCommande = models.CharField(max_length=42, default='Null')
    quantiteCommandeRecue = models.CharField(max_length=42, default='Null')
    quantiteDifference = models.CharField(max_length=42, default='Null')
    quantiteDifferenceAutre = models.CharField(max_length=42, default='Null')
    quantiteDifferenceRestante = models.CharField(max_length=42, default='Null')
    quantiteProduit = models.CharField(max_length=42, default='Null')
    quantiteProduitALivrer = models.CharField(max_length=42, default='Null')
    quantiteProduitLitige = models.CharField(max_length=42, default='Null')
    quantiteProduitRecu = models.CharField(max_length=42, default='Null')
    quantiteRecue = models.CharField(max_length=42, default='Null')
    termine = models.CharField(max_length=42, default='Null')

#End of BonCommandeEntree

#Models for LettreVoitureEntree
class LettreVoitureEntree(models.Model):
    idLettreVoitureEntree = models.CharField(max_length=42, default='Null')
    fk_Transporteur = models.ForeignKey('Transporteur_pour_LettreVoitureEntree', on_delete=models.CASCADE, default=0)
    def __str__(self):
        return self.idLettreVoitureEntree

class BonLivraisonEntree_pour_LettreVoitureLettreVoitureEntree(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=42, default='Null')
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.CASCADE, default=0)
    fk_Client = models.ForeignKey('Client_pour_LettreVoitureEntree', on_delete=models.CASCADE, default=0)
    def __str__(self):
        return self.idBonLivraisonEntree

class Client_pour_LettreVoitureEntree(models.Model):
    idClient = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idClient

class OrdreTransport_pour_LettreVoitureEntree(models.Model):
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.CASCADE, default=0)

class Transporteur_pour_LettreVoitureEntree(models.Model):
    idTransporteur = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idTransporteur

#End of LettreVoitureEntree


class Transporteur(models.Model):
    idTransporteur = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

#article
class Article(models.Model):
    idArticle = models.CharField(max_length=42, default='Null')
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, default=0, blank=True, null=True)
    #fk_Fournisseur = models.ForeignKey('Fournisseur_pour_Article', on_delete=models.CASCADE, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    codeFournisseur = models.CharField(max_length=42, default='Null')
    codeClient = models.CharField(max_length=42, default='Null')
    designationFournisseur = models.CharField(max_length=42, default='Null')
    designationClient = models.CharField(max_length=42, default='Null')
    dureeStockage = models.CharField(max_length=42, default='Null')
    delaiPeremption = models.CharField(max_length=42, default='Null')
    stock = models.CharField(max_length=42, default='Null')
    poidsColisStandard = models.CharField(max_length=42, default='Null')
    quantiteColisStandard = models.CharField(max_length=42, default='Null')
    quantiteColisStockComplet = models.CharField(max_length=42, default='Null')
    quantiteProduitStockComplet = models.CharField(max_length=42, default='Null')
    quantiteColisStockIncomplet = models.CharField(max_length=42, default='Null')
    quantiteProduitStockIncomplet = models.CharField(max_length=42, default='Null')
    quantiteUniteManutentionSortie = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.designationClient

class Colis_pour_Article(models.Model):
    fk_Article = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idColis = models.CharField(max_length=42, default='Null')
    fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.CASCADE, default=0)
    """fk_UniteManutentionSortie = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)
    fk_EtiquetteColis = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)
    fk_ColisStandard = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)
    fk_litige = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)
    fk_litigeDecision = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)
    fk_Colis = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)"""
    #fk_ZoneDepot = models.ForeignKey('ZoneDepot_pour_UniteManutentionEntree_colis', on_delete=models.CASCADE, default=0)
    emplacementConfirme = models.CharField(max_length=42, default='Null')
    numeroLot = models.CharField(max_length=42, default='Null')
    datePeremption = models.CharField(max_length=42, default='Null')
    quantiteProduit = models.CharField(max_length=42, default='Null')
    numerotation = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idColis

class Article_historique_pour_Article(models.Model):
    fk_Article = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, default=0)
    #fk_Fournisseur = models.ForeignKey('Fournisseur_pour_Article_historique', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idArticle_historique = models.CharField(max_length=42, default='Null')
    nomFournisseur = models.CharField(max_length=42, default='Null')
    codeFournisseur = models.CharField(max_length=42, default='Null')
    designationFournisseur = models.CharField(max_length=42, default='Null')
    codeClient = models.CharField(max_length=42, default='Null')
    designationClient = models.CharField(max_length=42, default='Null')
    poids = models.CharField(max_length=42, default='Null')
    delaiPeremption = models.CharField(max_length=42, default='Null')
    dureeStockage = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idArticle_historique

class Fournisseur_pour_Article_historique(models.Model):
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    #fk_type = models.ForeignKey('#', on_delete=models.CASCADE, default=0)
    idFournisseur = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class Article_Destinataire_pour_Article(models.Model):
    fk_Article = models.ForeignKey('Article', on_delete=models.CASCADE, default=0)
    fk_Destinataire = models.ForeignKey('Destinataire_pour_Article', on_delete=models.CASCADE, default=0)
    idArticle_Destinataire = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    delaiPeremption = models.CharField(max_length=42, default='Null')
    #Rubrique11 = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idArticle_Destinataire

class Destinataire_pour_Article(models.Model):
    idDestinataire = models.CharField(max_length=42, default='Null')
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.CASCADE, default=0)
    #fk_BonLivraisonEntree = models.ForeignKey('client_pour_import_boncommandesortie', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    adresseLivraison = models.CharField(max_length=42, default='Null')
    adresseFacturation = models.CharField(max_length=42, default='Null')
    departement = models.CharField(max_length=42, default='Null')
    telephone = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    identifiantBonLivraison = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    codeUM = models.CharField(max_length=42, default='Null')
    email = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    adresseLivraison_nom = models.CharField(max_length=42, default='Null')
    adresseLivraison_numero = models.CharField(max_length=42, default='Null')
    adresseLivraison_rue = models.CharField(max_length=42, default='Null')
    adresseLivraison_complement_1 = models.CharField(max_length=42, default='Null')
    adresseLivraison_complement_2 = models.CharField(max_length=42, default='Null')
    adresseLivraison_codePostal = models.CharField(max_length=42, default='Null')
    adresseLivraison_localite = models.CharField(max_length=42, default='Null')
    fk_Pays = models.ForeignKey('Pays_pour_Destinataire', on_delete=models.CASCADE, default=0)
    delaiPeremption = models.CharField(max_length=42, default='Null')
    ordreTri = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class Client_pour_Article_typeDestinataire(models.Model):
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idClient = models.CharField(max_length=42, default='Null')
    fk_TypeZone = models.ForeignKey('TypeZoneDepot', on_delete=models.CASCADE, default=0)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.CASCADE, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.CASCADE, default=0)
    nom = models.CharField(max_length=42, default='Null')
    adress = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    telephone = models.CharField(max_length=42, default='Null')
    email = models.CharField(max_length=42, default='Null')
    siret = models.CharField(max_length=42, default='Null')
    tva = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    nomCompte = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class Fournisseur_pour_Article(models.Model):
    idFournisseur = models.CharField(max_length=42, default='Null')
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class Client_pour_Article_typeArticle(models.Model):
    fk_TypeZone = models.ForeignKey('TypeZoneDepot', on_delete=models.CASCADE, default=0)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.CASCADE, default=0)
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.CASCADE, default=0)
    fk_TypeArticle = models.ForeignKey('typeArticle_pour_Article', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idClient = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    adress = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    telephone = models.CharField(max_length=42, default='Null')
    email = models.CharField(max_length=42, default='Null')
    siret = models.CharField(max_length=42, default='Null')
    tva = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    nomCompte = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class typeArticle_pour_Article(models.Model):
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idTypeArticle = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

#endof article

#Destinataire
class Destinataire(models.Model):
    idDestinataire = models.CharField(max_length=42, default='Null')
    fk_Pays = models.ForeignKey('Pays_pour_Destinataire', on_delete=models.CASCADE, default=0)
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    adresseLivraison = models.CharField(max_length=42, default='Null')
    adresseFacturation = models.CharField(max_length=42, default='Null')
    departement = models.CharField(max_length=42, default='Null')
    telephone = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    identifiantBonLivraison = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    codeUM = models.CharField(max_length=42, default='Null')
    email = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    adresseLivraison_nom = models.CharField(max_length=42, default='Null')
    adresseLivraison_numero = models.CharField(max_length=42, default='Null')
    adresseLivraison_rue = models.CharField(max_length=42, default='Null')
    adresseLivraison_complement_1 = models.CharField(max_length=42, default='Null')
    adresseLivraison_complement_2 = models.CharField(max_length=42, default='Null')
    adresseLivraison_codePostal = models.CharField(max_length=42, default='Null')
    adresseLivraison_localite = models.CharField(max_length=42, default='Null')
    delaiPeremption = models.CharField(max_length=42, default='Null')
    ordreTri = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class BonCommandeSortie_pour_Destinataire(models.Model):
    idBonCommandeSortie = models.CharField(max_length=42, default='Null')
    fk_Destinataire = models.ForeignKey('Destinataire', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    #fk_Client = models.ForeignKey('Destinataire', on_delete=models.CASCADE, default=0)
    #fk_Destinataire = models.ForeignKey('Destinataire', on_delete=models.CASCADE, default=0)
    #fk_Transporteur = models.ForeignKey('Destinataire', on_delete=models.CASCADE, default=0)
    #fk_TypeBonCommandeSortie = models.ForeignKey('Destinataire', on_delete=models.CASCADE, default=0)
    numeroCommande = models.CharField(max_length=42, default='Null')
    dateCommande = models.CharField(max_length=42, default='Null')
    termine = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.numeroCommande

class UniteManutentionSortie_pour_Destinataire(models.Model):
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_Destinataire', on_delete=models.CASCADE, default=0)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idUniteManutentionSortie = models.CharField(max_length=42, default='Null')
    #fk_TypeUniteManutention = models.ForeignKey('', on_delete=models.CASCADE, default=0)
    #fk_BonLivraisonSortie = models.ForeignKey('', on_delete=models.CASCADE, default=0)
    #fk_Etiquette = models.ForeignKey('', on_delete=models.CASCADE, default=0)
    numero = models.CharField(max_length=42, default='Null')
    dateOuverture = models.CharField(max_length=42, default='Null')
    dateFermeture = models.CharField(max_length=42, default='Null')
    dateExpedition = models.CharField(max_length=42, default='Null')
    poidsBrut = models.CharField(max_length=42, default='Null')
    poidsTare = models.CharField(max_length=42, default='Null')
    poidsNet = models.CharField(max_length=42, default='Null')
    poidsDifference = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.numero

class TypeDestinataire_pour_Destinataire(models.Model):
    idTypeDestinataire = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class Pays_pour_Destinataire(models.Model):
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idPays = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    codeISO_2 = models.CharField(max_length=42, default='Null')
    codeISO_3 = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom
    #endof destinataire

#Start Client

class Client(models.Model):
    idClient = models.CharField(max_length=42, default='Null')
    fk_TypeZone = models.ForeignKey('TypeZoneDepot_pour_Client', on_delete=models.CASCADE, default=1)
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Client', on_delete=models.CASCADE, default=1)
    fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Client', on_delete=models.CASCADE, default=1)
    fk_TypeArticle = models.ForeignKey('TypeArticle_pour_Client', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    adresse = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    telephone = models.CharField(max_length=42, default='Null')
    email = models.CharField(max_length=42, default='Null')
    siret = models.CharField(max_length=42, default='Null')
    tva = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    nomCompte = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class BonCommandeSortie_pour_Client(models.Model):
    fk_Client = models.ForeignKey('Client', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idBonCommandeSortie = models.CharField(max_length=42, default='Null')
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, default=1)
    fk_TypeBonCommandeSortie = models.ForeignKey('TypeBonCommandeSortie_pour_BonCommandeSortie', on_delete=models.CASCADE, default=1)
    fk_Destinataire = models.ForeignKey('Destinataire', on_delete=models.CASCADE, default=1)
    numeroCommande = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idBonCommandeSortie

class BonLivraisonEntree_pour_Client(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=42, default='Null')
    fk_Client = models.ForeignKey('Client', on_delete=models.CASCADE, default=1)
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.CASCADE, default=1)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, default=1)
    #fk_Destinataire_litige = models.ForeignKey('Destinataire_pour_BonLivraisonEntree', on_delete=models.CASCADE, default=1)
    #fk_ZoneDepot_litige = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, default=1)
    dateReception = models.CharField(max_length=42, default='Null')
    numeroBonLivraison = models.CharField(max_length=42, default='Null')
    quantitePalette = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')

class OrdreTransport_pour_Client(models.Model):
    idOrdreTransport = models.CharField(max_length=42, default='Null')
    fk_Client = models.ForeignKey('Client', on_delete=models.CASCADE, default=1)
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.CASCADE, default=1)
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    dateCreation = models.CharField(max_length=42, default='Null')

class Contact_pour_Client(models.Model):
    idContact = models.CharField(max_length=42, default='Null')
    fk_Client = models.ForeignKey('Client', on_delete=models.CASCADE, default=1)
    fk_RoleContact = models.ForeignKey('RoleContact_pour_Client', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    prenom = models.CharField(max_length=42, default='Null')
    telephone = models.CharField(max_length=42, default='Null')
    email = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class RoleContact_pour_Client(models.Model):
    idRoleContact = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class TypeZoneDepot_pour_Client(models.Model):
    idTypeZoneDepot = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')

class TypeFournisseur_pour_Client(models.Model):
    idTypeFournisseur = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')

class TypeDestinataire_pour_Client(models.Model):
    idTypeFournisseur = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')

class TypeArticle_pour_Client(models.Model):
    idTypeArticle = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')

#end of Client

#ressource
class TypeZoneDepot(models.Model):
    idTypeZoneDepot = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class ZoneDepot_pour_TypeZoneDepot(models.Model):
    fk_TypeZoneDepot = models.ForeignKey('TypeZoneDepot', on_delete=models.CASCADE, default=1)
    idZoneDepot = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class TypeFournisseur_pour_Fournisseur(models.Model):
    idTypeFournisseur = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class Fournisseur(models.Model):
    idFournisseur = models.CharField(max_length=42, default='Null')
    fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class TypeBonCommandeSortie_pour_BonCommandeSortie(models.Model):
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idTypeBonCommandeSortie = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

#Unitemanutentionentree debut
class UniteManutentionEntree(models.Model):
    idUnitManutentionEntree = models.CharField(max_length=42, default='Null')
    fk_BonLivraisonEntree = models.ForeignKey('BonLivraisonEntree_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_ZoneDepot = models.ForeignKey('ZoneDepot_pour_UniteManutentionEntree_colis', on_delete=models.CASCADE, default=1)
    #plutôt que de faire des one to many je vais faire des tables indépendantes relié par moi
    #fk_Etiquette = models.ForeignKey('EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    numero = models.CharField(max_length=42, default='Null')
    dateReception = models.CharField(max_length=42, default='Null')
    stock = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.numero

class Colis_pour_UniteManutentionEntree(models.Model):
    idColis = models.CharField(max_length=42, default='Null')
    #fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_UniteManutentionSortie = models.ForeignKey('UniteManutentionSortie_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_EtiquetteColis = models.ForeignKey('EtiquetteColis_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_Article = models.ForeignKey('Article_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_litige = models.ForeignKey('Litige_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_LitigeDecision = models.ForeignKey('LitigeDecision_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    #fk_ZoneDepot = models.ForeignKey('ZoneDepot_pour_UniteManutentionEntree_colis', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    #fk_Colis = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    #fk_ColisStandard = models.ForeignKey('', on_delete=models.CASCADE, default=1)
    emplacementConfirme = models.CharField(max_length=42, default='Null')
    numeroLot = models.CharField(max_length=42, default='Null')
    datePeremption = models.CharField(max_length=42, default='Null')
    quantiteProduit = models.CharField(max_length=42, default='Null')
    numerotation = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idClois

class EtiquetteColis_pour_UniteManutentionEntree_historique(models.Model):
    fk_Colis = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idEtiquetteColis = models.CharField(max_length=42, default='Null')
    expediteur = models.CharField(max_length=42, default='Null')
    codeArticleFournisseur = models.CharField(max_length=42, default='Null')
    nomCompte = models.CharField(max_length=42, default='Null')
    quantiteProduit = models.CharField(max_length=42, default='Null')
    numeroLot = models.CharField(max_length=42, default='Null')
    datePeremption = models.CharField(max_length=42, default='Null')
    designationArticleFournisseur = models.CharField(max_length=42, default='Null')
    codeUM = models.CharField(max_length=42, default='Null')
    Fournisseur = models.CharField(max_length=42, default='Null')
    datamatrix_humaine = models.CharField(max_length=42, default='Null')
    retour = models.CharField(max_length=42, default='Null')
    collee = models.CharField(max_length=42, default='Null')
    afficherExpediteur = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class Colis_ZoneDepot_pour_UniteManutentionEntree(models.Model):
    fk_Colis = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idColis_ZoneDepot = models.CharField(max_length=42, default='Null')
    fk_ZoneDepot = models.ForeignKey('ZoneDepot_pour_UniteManutentionEntree_colis', on_delete=models.CASCADE, default=1)
    dateEntree = models.CharField(max_length=42, default='Null')
    dateSortie = models.CharField(max_length=42, default='Null')
    #def __str__(self):
        #return self.nom

class Colis_UniteManutentionSortie_pour_UniteManutentionEntree(models.Model):
    fk_Colis = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_UniteManutentionSortie = models.ForeignKey('UniteManutentionSortie_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    idColis_UniteManutentionSortie = models.CharField(max_length=42, default='Null')


class UniteManutentionSortie_pour_UniteManutentionEntree(models.Model):
    idColis = models.CharField(max_length=42, default='Null')
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)

class BonCommandeSortie_pour_UniteManutentionEntree(models.Model):
    idBonCommandeSortie = models.CharField(max_length=42, default='Null')
    fk_Destinataire = models.ForeignKey('Destinataire_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_TypeBonCommandeSortie = models.ForeignKey('TypeBonCommandeSortie_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)

class Destinataire_pour_UniteManutentionEntree(models.Model):
    idDestinataire = models.CharField(max_length=42, default='Null')

class TypeBonCommandeSortie_pour_UniteManutentionEntree(models.Model):
    idTypeBonCommandeSortie = models.CharField(max_length=42, default='Null')

class EtiquetteColis_pour_UniteManutentionEntree(models.Model):
    idEtiquetteColis = models.CharField(max_length=42, default='Null')

class Article_pour_UniteManutentionEntree(models.Model):
    idArticle = models.CharField(max_length=42, default='Null')
    fk_Fournisseur = models.ForeignKey('Fournisseur_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_TypeFournisseur = models.ForeignKey('TypeArticle_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)

class Fournisseur_pour_UniteManutentionEntree(models.Model):
    idFournisseur = models.CharField(max_length=42, default='Null')

class TypeArticle_pour_UniteManutentionEntree(models.Model):
    idTypeArticle = models.CharField(max_length=42, default='Null')

class Litige_pour_UniteManutentionEntree(models.Model):
    idLitige = models.CharField(max_length=42, default='Null')

class LitigeDecision_pour_UniteManutentionEntree(models.Model):
    idLitigeDecision = models.CharField(max_length=42, default='Null')

class ZoneDepot_pour_UniteManutentionEntree_colis(models.Model):
    idZoneDepot = models.CharField(max_length=42, default='Null')
    fk_TypeZoneDepot = models.ForeignKey('TypeZoneDepot_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class LotRetire_pour_UniteManutentionEntree_pour_UniteManutentionEntree_historique(models.Model):
    fk_Article = models.ForeignKey('UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    numeroLot = models.ForeignKey('Colis_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    idLotRetire = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idLotRetire

class EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree_historique(models.Model):
    fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idEtiquetteUniteManutentionEntree = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idEtiquetteUniteManutentionEntree

class BonLivraisonEntree_pour_UniteManutentionEntree(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=42, default='Null')
    fk_Client = models.ForeignKey('Client_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    fk_Destinataire_litige = models.ForeignKey('Destinataire_pour_UniteManutentionEntree_litige', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    #fk_LettreVoitureEntree = models.ForeignKey('', on_delete=models.CASCADE, default=1)
    #fk_Fournisseur = models.ForeignKey('', on_delete=models.CASCADE, default=1)
    #fk_ZoneDepot_litige = models.ForeignKey('', on_delete=models.CASCADE, default=1)
    dateReception = models.CharField(max_length=42, default='Null')
    numeroBonLivraison = models.CharField(max_length=42, default='Null')
    quantitePalette = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.idBonLivraisonEntree

class Client_pour_UniteManutentionEntree(models.Model):
    idClient = models.CharField(max_length=42, default='Null')
    fk_TypeZone = models.ForeignKey('TypeZoneDepot_pour_UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    #fk_TypeFournisseur = models.ForeignKey('TypeFournisseur_pour_Fournisseur', on_delete=models.CASCADE, default=1)
    #fk_TypeDestinataire = models.ForeignKey('TypeDestinataire_pour_Destinataire', on_delete=models.CASCADE, default=1)
    #fk_TypeArticle = models.ForeignKey('TypeArticle_pour_Article', on_delete=models.CASCADE, default=1)
    nom = models.CharField(max_length=42, default='Null')
    adresse = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    telephone = models.CharField(max_length=42, default='Null')
    email = models.CharField(max_length=42, default='Null')
    siret = models.CharField(max_length=42, default='Null')
    tva = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    nomCompte = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class Destinataire_pour_UniteManutentionEntree_litige(models.Model):
    idDestinataire = models.CharField(max_length=42, default='Null')
    #fk_TypeDestinataire = models.ForeignKey('', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    adresseLivraison = models.CharField(max_length=42, default='Null')
    adresseFacturation = models.CharField(max_length=42, default='Null')
    departement = models.CharField(max_length=42, default='Null')
    telephone = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    identifiantBonLivraison = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    codeUM = models.CharField(max_length=42, default='Null')
    email = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    adresseLivraison_nom = models.CharField(max_length=42, default='Null')
    adresseLivraison_numero = models.CharField(max_length=42, default='Null')
    adresseLivraison_rue = models.CharField(max_length=42, default='Null')
    adresseLivraison_complement_1 = models.CharField(max_length=42, default='Null')
    adresseLivraison_complement_2 = models.CharField(max_length=42, default='Null')
    adresseLivraison_codePostal = models.CharField(max_length=42, default='Null')
    adresseLivraison_localite = models.CharField(max_length=42, default='Null')
    fk_Pays = models.ForeignKey('Pays_pour_Destinataire', on_delete=models.CASCADE, default=1)
    delaiPeremption = models.CharField(max_length=42, default='Null')
    ordreTri = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class TypeZoneDepot_pour_UniteManutentionEntree(models.Model):
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    idTypeZoneDepot = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class ZoneDepot_pour_UniteManutentionEntree(models.Model):
    idZoneDepot = models.CharField(max_length=42, default='Null')
    #fk_TypeZoneDepot = models.ForeignKey('', on_delete=models.CASCADE, default=1)
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nom

class EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree(models.Model):
    #fk_UniteManutentionEntree = models.ForeignKey('UniteManutentionEntree', on_delete=models.CASCADE, default=1)
    idEtiquetteUniteManutentionEntree = models.CharField(max_length=42, default='Null')
    c_nom = models.CharField(max_length=42, default='Null')
    c_nomCompte = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    m_nom = models.CharField(max_length=42, default='Null')
    m_nomCompte = models.CharField(max_length=42, default='Null')
    m_horodatage = models.CharField(max_length=42, default='Null')
    client = models.CharField(max_length=42, default='Null')
    numeroUM = models.CharField(max_length=42, default='Null')
    zone = models.CharField(max_length=42, default='Null')
    fournisseur = models.CharField(max_length=42, default='Null')
    quantiteColis = models.CharField(max_length=42, default='Null')
    dateReception = models.CharField(max_length=42, default='Null')
    nomCompte = models.CharField(max_length=42, default='Null')
    collee = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.nomCompte
#fin

#début Colis
class Colis(models.Model):
    idColis = models.CharField(max_length=42, default='Null')

#fin

#début Bon Livraison Sortie

class BonLivraisonSortie(models.Model):
    idBonLivraisonSortie = models.CharField(max_length=42, default='Null')
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_BonLivraisonSortie', on_delete=models.CASCADE, default=1)
    fk_LettreVoitureSortie = models.ForeignKey('LettreVoitureSortie_pour_BonLivraisonSortie', on_delete=models.CASCADE, default=1)
    dateImpression = models.CharField(max_length=42, default='Null')
    numeroBonLivraison = models.CharField(max_length=42, default='Null')
    prixExpedition = models.CharField(max_length=42, default='Null')
    codeTracking = models.CharField(max_length=42, default='Null')
    c_horodatage = models.CharField(max_length=42, default='Null')
    #fk_Transporteur = models.ForeignKey('', on_delete=models.CASCADE, default=1)

class UniteManutentionSortie_pour_BonLivraisonSortie(models.Model):
    idUniteManutentionSortie = models.CharField(max_length=42, default='Null')
    fk_BonLivraisonSortie = models.ForeignKey('Colis_pour_BonLivraisonSortie', on_delete=models.CASCADE, default=1)
    numero = models.CharField(max_length=42, default='Null')

class Colis_pour_BonLivraisonSortie(models.Model):
    idColis = models.CharField(max_length=42, default='Null')
    #fk_UniteManutentionSortie = models.ForeignKey('UniteManutentionSortie_pour_BonLivraisonSortie', on_delete=models.CASCADE, default=1)
    fk_Article = models.ForeignKey('Article_pour_BonLivraisonSortie_Colis', on_delete=models.CASCADE, default=1)

class Article_pour_BonLivraisonSortie_Colis(models.Model):
    idArticle = models.CharField(max_length=42, default='Null')


class LigneBonLivraisonSortie_pour_BonLivraisonSortie(models.Model):
    idLigneBonLivraisonSortie = models.CharField(max_length=42, default='Null')
    fk_BonLivraisonSortie = models.ForeignKey('UniteManutentionSortie_pour_BonLivraisonSortie', on_delete=models.CASCADE, default=1)
    fk_Article = models.ForeignKey('Article_pour_BonLivraisonSortie', on_delete=models.CASCADE, default=1)
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, default=1)
    quantiteColis = models.CharField(max_length=42, default='Null')
    stat_quantiteColis = models.CharField(max_length=42, default='Null')

class Article_pour_BonLivraisonSortie(models.Model):
    idArticle = models.CharField(max_length=42, default='Null')

class BonCommandeSortie_pour_BonLivraisonSortie(models.Model):
    idBonCommandeSortie = models.CharField(max_length=42, default='Null')
    fk_Client = models.ForeignKey('Client_pour_BonLivraisonSortie', on_delete=models.CASCADE, default=1)
    fk_Destinataire = models.ForeignKey('Destinataire_pour_BonLivraisonSortie', on_delete=models.CASCADE, default=1)

class LigneBonCommandeSortie_pour_BonLivraisonSortie(models.Model):
    fk_BonCommandeSortie = models.ForeignKey('BonCommandeSortie_pour_BonLivraisonSortie', on_delete=models.CASCADE, default=1)
    idLigneBonCommandeSortie = models.CharField(max_length=42, default='Null')

class Client_pour_BonLivraisonSortie(models.Model):
    idClient = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')

class Destinataire_pour_BonLivraisonSortie(models.Model):
    idDestinataire = models.CharField(max_length=42, default='Null')
    nom = models.CharField(max_length=42, default='Null')
    identifiantBonLivraison = models.CharField(max_length=42, default='Null')
    codeUM = models.CharField(max_length=42, default='Null')

class LettreVoitureSortie_pour_BonLivraisonSortie(models.Model):
    idLettreVoitureSortie = models.CharField(max_length=42, default='Null')
    numeroRecepisse = models.CharField(max_length=42, default='Null')

class BonCommandeSortie(models.Model):
    idBonCommandeSortie = models.CharField(max_length=42, default='Null')
    termine = models.CharField(max_length=42, default='Null')
    source = models.CharField(max_length=42, default='Null')
    identifiantSource = models.CharField(max_length=42, default='Null')
    numeroCommande = models.CharField(max_length=42, default='Null')
    dateCommande = models.CharField(max_length=42, default='Null')
    fk_Client = models.ForeignKey('Client', on_delete=models.CASCADE, default=1)
    fk_Destinataire = models.ForeignKey('Destinataire', on_delete=models.CASCADE, default=1)
    fk_Transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, default=1)
    fk_TypeBonCommandeSortie = models.ForeignKey('TypeBonCommandeSortie_pour_BonCommandeSortie', on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.numeroCommande

class BonLivraisonEntree(models.Model):
    idBonLivraisonEntree = models.CharField(max_length=42, default='Null')
    fk_LettreVoitureEntree = models.ForeignKey('LettreVoitureEntree', on_delete=models.CASCADE, default=1)
    fk_Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, default=1)
    fk_Client = models.ForeignKey('Client', on_delete=models.CASCADE, default=1)
    dateReception = models.CharField(max_length=42, default='Null')
    numeroBonLivraison = models.CharField(max_length=42, default='Null')
    quantitePalette = models.CharField(max_length=42, default='Null')
    commentaire = models.CharField(max_length=42, default='Null')
    def __str__(self):
        return self.numeroBonLivraison
