from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from datetime import date

class User(AbstractUser):
    is_partenaire = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_transporteur = models.BooleanField(default=False)
    nom = models.CharField(max_length=100)
    coordonnee = models.PointField(null=True, blank=True)
    adresse = models.CharField(max_length=100)
    
    
    


class Schedule(models.Model):
    name = models.CharField(max_length=255)
    date_from = models.DateField("date from", default=date.today)
    date_to = models.DateField("date to", default=date.today)
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name or self.__class__.__name__


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crossdocker = models.ManyToManyField('Partenaire', through='OffreLivraison', through_fields=('client','partenaire'))
    transporteurs = models.ManyToManyField('Transporteur', through='OffreCommandeLivraison', through_fields=('client','transporteur'))
    date = models.DateTimeField(default=timezone.now, 
                                verbose_name="Date d'inscription")
   

    class Meta:

        verbose_name = "Client"

        ordering = ['date']

    def __str__(self):
 
    
        return self.user.username

class Produit(models.Model):
    
    clientProp = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='produits')

    refproduit = models.CharField(max_length=30)
    
    designation = models.CharField(max_length=30)
    categorie = models.IntegerField(default=1,validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])
    photo = models.ImageField(upload_to="photos/",blank=True)
    
    

    def __str__(self):

        return self.designation 



class Partenaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    clientele = models.ManyToManyField('Client', through='OffreLivraison', through_fields=('partenaire','client'))
    date = models.DateTimeField(default=timezone.now, 
                                verbose_name="Date de creation")
    
    class Meta:

        verbose_name = "Partenaire"

        ordering = ['date']

    def __str__(self):

        return self.user.username

class Commande (models.Model):
    
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='commandes')
    partenaire = models.ForeignKey('Partenaire', on_delete=models.CASCADE, related_name='commandes')
    transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, related_name='commandes')
    refproduit = models.CharField(max_length=30)
    reference = models.CharField(max_length=30)
    destinataire = models.CharField(max_length=50)
    specifite = models.CharField(max_length=30)
    quantite = models.IntegerField(default=1)
    dateDepart = models.DateField()
   
    
    

    def __str__(self):

        return self.reference



class Entrepot(models.Model):
    partenaireProp = models.ForeignKey('Partenaire', on_delete=models.CASCADE, related_name='entrepots')
    designation = models.CharField(max_length=30)
   
    geom  = models.PointField(null=True, blank=True)
    adresse = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    capacite = models.IntegerField()
    specificite = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="photos/",blank=True)
    
    def __str__(self):

        return self.designation

class Transporteur (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clientele = models.ManyToManyField('Client', through='OffreCommandeLivraison', through_fields=('transporteur','client'))
    specificite = models.CharField(max_length=30)
    
    disponibilite = models.BooleanField('libre ?', default=True)
    
 
    def __str__(self):

        return self.user.nom


class Place(models.Model):
    partenaire = models.ForeignKey('Partenaire', on_delete=models.CASCADE, related_name='places')
    designation = models.CharField(max_length=30,null=True, blank=True)
    entrepot = models.ForeignKey('Entrepot', on_delete=models.CASCADE, related_name='places')
    refproduit = models.CharField(max_length=30,null=True, blank=True)
    destinataire = models.CharField(max_length=30,null=True, blank=True)
    categorie = models.CharField(max_length=30)
    nb_palettes = models.IntegerField(default=1)
    state = models.BooleanField('rempli ?', default=False)
 
    
    

    def __str__(self):

        return self.designation 
'''
#definition d'un gestionnaire personnalise
class TarifManager(models.Manager):
    def get_queryset(self):
        super().get_queryset().annotate(prixFinal=F('prix') + F('prix')*0.3)
'''

class SuiviStock (models.Model):
    
    refproduit = models.CharField(max_length=30)
    premiereentree = models.DateField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='suivistocks')
    entrepot = models.ForeignKey('Entrepot', on_delete=models.CASCADE, related_name='suivistocks')
    dernieremodification = models.DateField()
    quantitedispo = models.IntegerField(default=1)
    conditionnement = models.CharField(max_length=30)
    
    
    
    
    

    def __str__(self):

        return self.refproduit


class SuiviTransporteur (models.Model):
    
    designation = models.CharField(max_length=30)
    transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, related_name='suivitransports')
    entrepot = models.ForeignKey('Entrepot', on_delete=models.CASCADE, related_name='suivitransports')
    immatricule = models.CharField(max_length=30)
    livraison = models.BooleanField('livraison ?', default=False)
    enlevement = models.BooleanField('enlevement ?', default=False)
    date = models.DateField()
    nb_palettes = models.IntegerField(default=1)
   
    def __str__(self):

        return self.designation


class Tarif(models.Model):
    
    designation = models.CharField(max_length=30,null=True, blank=True)
    entrepot = models.ForeignKey('Entrepot', on_delete=models.CASCADE, related_name='tarifs')
    categorie = models.IntegerField(default=1,validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])
    nb_palettes = models.IntegerField(default=1)
    prix = models.IntegerField()
   
    #objects=TarifManager()
    
    

    def __str__(self):

        return self.designation 

class TarifTransport(models.Model):
    
    designation = models.CharField(max_length=30,null=True, blank=True)
    transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, related_name='tarifsTransport')
    depart = models.CharField(max_length=30,null=True, blank=True)
    arrive = models.CharField(max_length=30,null=True, blank=True)
    categorie = models.IntegerField(default=1,validators=[MinValueValidator(1),
                                       MaxValueValidator(2)])
    nb_palettes = models.IntegerField(default=1)
    prix = models.IntegerField()
   
    def __str__(self):

        return self.designation

class Camion(models.Model):
    
    designation = models.CharField(max_length=30,null=True, blank=True)
    transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, related_name='camions')
    matricule = models.CharField(max_length=30,null=True, blank=True)
    nb_palettes = models.IntegerField(default=8)
    photo = models.ImageField(upload_to="photos/",blank=True)
    disponible = models.BooleanField('disponible ?', default=True)
    plein = models.BooleanField('plein ?', default=False)
    
    def __str__(self):

        return self.designation

class Trajet(models.Model):
    
    voyage = models.CharField(max_length=30, blank=True)
    camion = models.ForeignKey('Camion', on_delete=models.CASCADE, related_name='camions')
  
    date = models.DateField(auto_now=True)
    effectue = models.BooleanField('effectue ?', default=False)
    encours = models.BooleanField('en cours ?', default=False)
   
    def __str__(self):

        return self.voyage

class OffreL(models.Model):
    designation = models.CharField(max_length=30)
    quantité = models.IntegerField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='offreC')
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, related_name='offreC')
    categorie = models.IntegerField(default=1,validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])
    datearrive = models.DateField()     
    
    def __str__(self):

        return self.designation

class OffreT(models.Model):
    designation = models.CharField(max_length=30)
    quantité = models.IntegerField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='offreT')
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, related_name='offreT')
    categorie = models.IntegerField(default=1,validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])
    depart = models.CharField(max_length=30,default="Paris")
    arrive = models.CharField(max_length=30,default="Paris")
    #revenir modifier
    adresse = models.CharField(max_length=150,default="50 rue de la place")
    adresse2 = models.CharField(max_length=150,default="500 rue de la République")
    
    datearrive = models.DateField()  
    livraison = models.BooleanField('livraison ?', default=True)  
    enlevement = models.BooleanField('enlevement ?', default=False)
    
    def __str__(self):

        return self.designation



class OffreLivraison(models.Model):
    
    partenaire = models.ForeignKey('Partenaire', on_delete=models.CASCADE, related_name='mesoffres')
    entrepot = models.ForeignKey('Entrepot', on_delete=models.CASCADE, related_name='mesoffres')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='mesoffres')
    offre = models.ForeignKey('OffreL', on_delete=models.CASCADE, related_name='mesoffres', null=True)
  
    
    Date = models.DateField(auto_now=True)
    

    

    def __str__(self):

        return self.offre.designation



class AcceptationLivraison(models.Model):
    partenaire = models.ForeignKey(Partenaire, on_delete=models.CASCADE, related_name='livraison_acceptations')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='livraison_acceptations')
    offre = models.ForeignKey(OffreLivraison, on_delete=models.CASCADE, related_name='livraison_acceptations')
    commentaire = models.CharField(max_length=150)

    is_accepted = models.BooleanField('accepter ?', default=False)

    Date = models.DateField(auto_now=True)
    def __str__(self):

        return self.commentaire




class OffreCommandeLivraison(models.Model):
    designation = models.CharField(max_length=30)
    offre = models.ForeignKey('OffreT', on_delete=models.CASCADE, related_name='livraisonTransport')
    
    
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='livraisonTransport')
    
    transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, related_name='livraisonTransport')
   
    date = models.DateField(auto_now=True)

    def __str__(self):

        return self.offre.designation

 

class AcceptationCommandeLivraison(models.Model):
    transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE, related_name='demmandeTransport')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='demmandeTransport')
    offre = models.ForeignKey(OffreCommandeLivraison, on_delete=models.CASCADE, related_name='demmandeTransport')
    commentaire = models.CharField(max_length=150)

    is_accepted = models.BooleanField('accepter ?', default=False)

    Date = models.DateField(auto_now=True)
    def __str__(self):

        return self.commentaire


class Appreciation(models.Model):
    message = models.CharField(max_length=150)
    
     
    qualite = models.IntegerField(default=0,validators=[MinValueValidator(0),
                                       MaxValueValidator(5)])
    partenaire = models.ForeignKey('Partenaire', on_delete=models.CASCADE, related_name='appreciation')
   
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='appreciation')
    
   
    
    Date = models.DateField(auto_now=True)

    def __str__(self):

        return self.message


class Message (models.Model):
    
    
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='utilisateur')
    text = models.TextField()
    Date = models.DateField(auto_now=True)

    def __str__(self):

        return self.text

class chose (models.Model):
    
    
    title = models.CharField(max_length=200)
    body = models.TextField()
    Date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):

        return self.title


class SendFile (models.Model):
    
    
   
    offre = models.ForeignKey(OffreLivraison, on_delete=models.CASCADE, related_name='livraison_files')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='livraison_files')
    partenaire = models.ForeignKey('Partenaire', on_delete=models.CASCADE, related_name='livraison_files')
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="photos/")

    def __unicode__(self):

        return self.offre.designation



