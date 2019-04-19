from django.contrib import admin
from django.utils.text import Truncator
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
# Register your models here.
from .models import OffreT,OffreL,User,SendFile,SuiviStock,Trajet,SuiviTransporteur,AcceptationCommandeLivraison,Camion,OffreCommandeLivraison,Place,TarifTransport,Message,Tarif,Transporteur,Commande,Appreciation,Client,Produit,Partenaire,Entrepot,OffreLivraison,AcceptationLivraison



   
admin.site.register(AcceptationCommandeLivraison )

admin.site.register(OffreCommandeLivraison )
admin.site.register(Commande )

admin.site.register(Place )
admin.site.register(Produit )

admin.site.register(SuiviStock )
admin.site.register(SuiviTransporteur )

admin.site.register(OffreLivraison )
admin.site.register(OffreL )
admin.site.register(OffreT )


admin.site.register(AcceptationLivraison )
admin.site.register(Partenaire )


admin.site.register(Camion )
admin.site.register(Trajet )
admin.site.register(Tarif )
admin.site.register(TarifTransport )

admin.site.register(Client )
admin.site.register(SendFile )
admin.site.register(Appreciation )


@admin.register(User)
class UserGeoAdmin(OSMGeoAdmin):
    list_display = ("nom", "adresse")

@admin.register(Entrepot)
class EntrepotGeoAdmin(OSMGeoAdmin):
    list_display = ("designation", "adresse")


admin.site.register(Transporteur)
admin.site.register(Message)
