from django.contrib import admin
from .models import *

# Register your models here.                                                        Si c'est en commentaire c'est que ce n'est pas utilisé ou inutile
admin.site.register(BonCommandeSortie)
admin.site.register(import_BonCommandeSortie)
admin.site.register(import_LigneBonCommandeSortie_pour_import_BonCommandeSortie)
#admin.site.register(BonCommandeSortie_pour_import_BonCommandeSortie)
admin.site.register(LigneBonCommandeSortie_pour_import_BonCommandeSortie)
#admin.site.register(Article_pour_BonCommandeSortie)
#admin.site.register(Client_pour_import_BonCommandeSortie)
#admin.site.register(Destinataire_pour_import_BonCommandeSortie)
#admin.site.register(TypeDestinataire_pour_BonCommandeSortie)
#admin.site.register(Destinataire_pour_Article)
#admin.site.register(UniteManutentionSortie_pour_BonCommandeSortie)
#admin.site.register(BonLivraisonSortie_pour_BonCommandeSortie)
admin.site.register(BonLivraisonEntree)
admin.site.register(LigneBonLivraisonEntree_pour_BonLivraisonEntree)
admin.site.register(BonCommandeEntree)
admin.site.register(LigneBonCommandeEntree_pour_BonCommandeEntree)
#admin.site.register(Article_pour_BonCommandeEntree)
#admin.site.register(BonCommandeEntree_BonLivraisonEntree_pour_BonCommandeEntree)
#admin.site.register(BonLivraisonEntree_pour_BonCommandeEntree)
#admin.site.register(UniteManutentionEntree_pour_BonCommandeEntree)
#admin.site.register(Colis_pour_BonCommandeEntree)
#admin.site.register(LigneBonLivraisonEntree_pour_BonCommandeEntree)
admin.site.register(LettreVoitureEntree)
admin.site.register(Article)
admin.site.register(typeArticle_pour_Article)
admin.site.register(Fournisseur)
admin.site.register(TypeFournisseur_pour_Fournisseur)
admin.site.register(Destinataire)
admin.site.register(Pays_pour_Destinataire)
admin.site.register(TypeDestinataire_pour_Destinataire)
#admin.site.register(UniteManutentionSortie_pour_Destinataire)
#admin.site.register(BonCommandeSortie_pour_Destinataire)
#admin.site.register(Transporteur_pour_import_BonCommandeSortie)
#admin.site.register(TypeBonCommandeSortie_pour_BonCommandeSortie)
admin.site.register(TypeZoneDepot)
admin.site.register(UniteManutentionEntree)
#admin.site.register(Colis_pour_UniteManutentionEntree)
#admin.site.register(EtiquetteColis_pour_UniteManutentionEntree_historique)
#admin.site.register(Colis_ZoneDepot_pour_UniteManutentionEntree)
#admin.site.register(Colis_UniteManutentionSortie_pour_UniteManutentionEntree)
#admin.site.register(UniteManutentionSortie_pour_UniteManutentionEntree)
#admin.site.register(BonCommandeSortie_pour_UniteManutentionEntree)
#admin.site.register(Destinataire_pour_UniteManutentionEntree)
#admin.site.register(TypeBonCommandeSortie_pour_UniteManutentionEntree)
#admin.site.register(EtiquetteColis_pour_UniteManutentionEntree)
#admin.site.register(Article_pour_UniteManutentionEntree)
#admin.site.register(Fournisseur_pour_UniteManutentionEntree)
#admin.site.register(TypeArticle_pour_UniteManutentionEntree)
#admin.site.register(Litige_pour_UniteManutentionEntree)
#admin.site.register(LitigeDecision_pour_UniteManutentionEntree)
#admin.site.register(ZoneDepot_pour_UniteManutentionEntree_colis)
#admin.site.register(LotRetire_pour_UniteManutentionEntree_pour_UniteManutentionEntree_historique)
#admin.site.register(EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree_historique)
#admin.site.register(BonLivraisonEntree_pour_UniteManutentionEntree)
#admin.site.register(Client_pour_UniteManutentionEntree)
#admin.site.register(Destinataire_pour_UniteManutentionEntree_litige)
#admin.site.register(TypeZoneDepot_pour_UniteManutentionEntree)
#admin.site.register(ZoneDepot_pour_UniteManutentionEntree)
#admin.site.register(EtiquetteUniteManutentionEntree_pour_UniteManutentionEntree)   
admin.site.register(BonLivraisonSortie)
#admin.site.register(BonCommandeSortie_pour_BonLivraisonSortie)
#admin.site.register(LettreVoitureSortie_pour_BonLivraisonSortie)
#admin.site.register(Client_pour_BonLivraisonSortie)
#admin.site.register(Destinataire_pour_BonLivraisonSortie)
admin.site.register(LigneBonLivraisonSortie_pour_BonLivraisonSortie)
#admin.site.register(UniteManutentionSortie_pour_BonLivraisonSortie)
#admin.site.register(Article_pour_BonLivraisonSortie)
#admin.site.register(LigneBonCommandeSortie_pour_BonLivraisonSortie)
#admin.site.register(Colis_pour_BonLivraisonSortie)
#admin.site.register(Article_pour_BonLivraisonSortie_Colis)
#admin.site.register(TypeUniteManutention_pour_UniteManutentionSortie)
admin.site.register(Transporteur)
admin.site.register(Client)
#admin.site.register(TypeZoneDepot_pour_Client)
#admin.site.register(TypeFournisseur_pour_Client)
#admin.site.register(TypeDestinataire_pour_Client)
#admin.site.register(TypeArticle_pour_Client)
admin.site.register(Contact_pour_Client)
admin.site.register(RoleContact_pour_Client)
admin.site.register(ZoneDepot_pour_TypeZoneDepot)

admin.site.register(imgaccueil)
