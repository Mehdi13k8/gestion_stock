from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import ListView

urlpatterns = [
    path('', views.index.as_view(), name='index'),

    #path('accounts/login/', auth_views.LoginView.as_view()),
    #path('login/', views.index_login.as_view(), name='login'),
    path('register', views.register.as_view(), name='register'),
    path('recregister/', views.recregister),
    path('delete_user/', views.deleteuser),

    path('create_typefour/', views.create_typef.as_view(), name='create_typefour'),
    path('create_typefour/add', views.create_typef_add.as_view(), name='create_new_typefour'),
    path('create_typefour_add/save/', views.create_typef_add.saveit),
    path('delete_typefour/delete/', views.create_typef.delete),

    path('modif_typefour/', views.modif_typef.as_view(), name='modif_typefour'),
    path('modif_typefour/save/', views.modif_typef.as_view(), name='modif_typefour_save'),

    path('zone_depot/', views.zonesdepot.as_view(), name='zonedepot'),
    path('zone_depot/create_zone/', views.zonesdepot.createnewzone),
    path('zone_depot/delete_zone/', views.zonesdepot.delete),

    path('type_destinataire/', views.typedest.as_view(), name='typedest'),
    path('type_destinataire/create_typedestinataire/', views.typedest.create),
    path('type_destinataire/delete_typedestinataire/', views.typedest.delete),

    path('type_article/', views.typeart.as_view(), name='typeart'),
    path('type_article/create_typearticle/', views.typeart.create),
    path('type_article/delete_typearticle/', views.typeart.delete),

    path('type_zone/', views.typezone.as_view(), name='typezone'),
    path('type_zone/create_typezone/', views.typezone.create),
    path('type_zone/delete_typezone/', views.typezone.delete),

    path('type_con/', views.typecont.as_view(), name='typecont'),
    path('type_con/create_typecont/', views.typecont.create),
    path('type_con/delete_typecont/', views.typecont.delete),

    path('pays/', views.pays.as_view(), name='pays'),
    path('pays/create_pays/', views.pays.create),
    path('pays/delete_pays/', views.pays.delete),

    path('settings/litiges', views.litiges.as_view(), name='litiges'),

    path('settings/litiges/addlitige', views.litigesadd.as_view(), name='litigesadd'),
    path('settings/litiges/addlitige/save/', views.litigesadd.create),

    path('settings/litiges/adddecilitige', views.decilitigesadd.as_view(), name='decilitigesadd'),
    path('settings/litiges/adddecilitige/save/', views.decilitigesadd.create),

    path('settings/litiges/modify', views.litigesmodify.as_view(), name='litigesmodify'),
    path('settings/litiges/litige/modify/save/', views.litigesmodify.modify),

    path('settings/decilitige/modify', views.decilitigesmodify.as_view(), name='decilitigesmodify'),
    path('settings/litiges/decilitige/modify/save/', views.decilitigesmodify.modify),


    #path('zone_depot/add', views.zonesdepotadd.as_view(), name='zonedepotadd'),
    #path('create_zonedepot/save/', views..saveit),
    #path('modif_zonedepot/', views.modif_zonedepot.as_view(), name='modif_'),
    #path('modif_zonedepot/save/', views.modif_zonedepot.as_view(), name='modif__save'),

    path('index', views.index.as_view()),
    #path('setting', views.setting.as_view(), name='setting'),
    path('setting/<int:pk>/', views.setting.as_view(), name='setting'),
    path('setting/reset/', views.setting.reset),
    #path('accueil/', views.setting.accueilchange),

    #path('settings/change/accueil/', views.setting.accueilchange), #renvoie vers la fonction qui changera l'image de l'accueil via settings.accueilchange

    path('bon_entree', views.BonCommandeEntree_index.as_view(), name='bonCommandeEntree'), #page des bon de commande entree
    path('bon_entree/add', views.BonCommandeEntreeadd.as_view(), name='bonCommandeEntreeadd'), #page des possibilité a ajouter au bon de commande entree
    path('bon_entree/adding/', views.BonCommandeEntreeadd.add), #fonction 'add' dans la view qui permet de "crée" dans la bdd l'objet

    path('bon_entree/modify', views.BonCommandeEntreemodify.as_view(), name='bonCommandeEntreemodify'),
    path('delete_bon_entree/', views.BonCommandeEntree_index.delete),

    path('bon_sortie', views.bonCommandeSortie.as_view(), name='bonCommandeSortie'), #page des bon de commande sortie
    path('bon_sortie/add', views.bonCommandeSortieadd.as_view(), name='bonCommandeSortieadd'),
    path('bon_sortie/adding/', views.bonCommandeSortieadd.add),
    path('bon_sortie/modify', views.bonCommandeSortiemodify.as_view(), name='bonCommandeSortiemodify'),
    path('bon_sortie/modify/termin/', views.bonCommandeSortiemodify.termin),
    path('bon_sortie/modify/creebls/', views.bonCommandeSortiemodify.creebonlivraisonsortie),
    path('bon_sortie/modify/recalcule/', views.bonCommandeSortiemodify.recalcule),
    path('delete_bon_sortie/', views.bonCommandeSortie.delete),

    path('uploadbc/', views.uploadbc),
    path('upload_bcsf/', views.bonCommandeSortie.upload_bcsf),#pour sauvegarder les images stockée dans les bcs

    path('bonLivraisonsortie', views.bonLivraisonSortie.as_view(), name='bonLivraisonSortie'),
    path('bonLivraisonsortie/add', views.bonLivraisonSortieadd.as_view(), name='bonLivraisonSortieadd'),
    path('bonLivraisonsortie/modify', views.bonLivraisonSortiemodify.as_view(), name='bonLivraisonSortiemodify'),
    path('upload_blsf/', views.bonLivraisonSortiemodify.upload_blsf),#pour sauvegarder les images stockée dans les bcs

    path('lettrevoitureentree', views.lettrevoitureentree.as_view(), name='lve'),
    path('lettrevoitureentree/modify', views.lettrevoitureentreemodify.as_view(), name='lvemodify'),
    path('lve/modify/', views.lettrevoitureentreemodify.modify),
    path('lve/modify/createbl/', views.lettrevoitureentreemodify.createbl),
    path('lve/modify/deletebl/', views.lettrevoitureentreemodify.deletebl),
    path('lettrevoitureentree/add', views.lettrevoitureentreeadd.as_view(), name='lveadd'),
    path('lve/create/', views.lettrevoitureentreeadd.create),
    path('lve/delete/', views.lettrevoitureentree.delete),
    path('upload_lvef/', views.lettrevoitureentreemodify.upload_lvef),#pour sauvegarder les images stocké dans les ble

    path('bonLivraisonentree', views.bonLivraisonEntree.as_view(), name='bonLivraisonEntree'),
    path('bonLivraisonentree/add', views.bonLivraisonEntreeadd.as_view(), name='bonLivraisonEntreeadd'),
    path('bonLivraisonentree/modify/', views.bonLivraisonentreemodify.as_view(), name='bonLivraisonEntreemodify'),
    path('right_ble/', views.bonLivraisonentreemodify.right),
    path('left_ble/', views.bonLivraisonentreemodify.left),
    path('ble/modify/', views.bonLivraisonentreemodify.modify),
    path('ble/delete/', views.bonLivraisonEntree.delete),
    path('ble/create/', views.bonLivraisonEntreeadd.create),
    path('ligneble/create/', views.bonLivraisonEntreeadd.createligne),
    path('ligneble/delete/', views.bonLivraisonEntreeadd.deleteligne),
    path('bonLivraisonentree/modify/createume/', views.bonLivraisonentreemodify.createume),
    path('bonLivraisonentree/modify/deleteume/', views.bonLivraisonentreemodify.deleteume),
    path('upload_blef/', views.upload_blef),#pour sauvegarder les images stocké dans les ble
    #path('upload_blef/redirect', views.upload_blef_redirect, name='uploadbleredirect'),#pour sauvegarder les images stocké dans les ble

    path('article', views.article.as_view(), name='article'),
    path('article/emplacement', views.articleemplacement.as_view(), name='articleparemplacement'),
    path('article/delete/', views.article.delete),
    path('article/add', views.articleadd.as_view(), name='articleadd'),
    path('article/add/create/', views.articleadd.create),
    path('article/modify', views.articlemodify.as_view(), name='articlemodify'),
    path('article/modify/modif/', views.articlemodify.modif),
    path('right_article/', views.articlemodify.right),
    path('left_article/', views.articlemodify.left),

    path('fournisseur', views.fournisseur.as_view(), name='fournisseur'),
    path('fournisseur/add', views.fournisseuradd.as_view(), name='fournisseuradd'),
    path('fournisseur/modify', views.fournisseurmodify.as_view(), name='fournisseurmodify'),
    path('right_fournisseur/', views.fournisseurmodify.right),
    path('left_fournisseur/', views.fournisseurmodify.left),
    path('modify_four/', views.fournisseurmodify.modify, name='fournisseurmodifysave'),
    path('create_four/', views.create_four),
    path('delete_four/', views.delete_four),

    path('transporteur', views.transporteur.as_view(), name='transporteur'),
    path('transporteur/add', views.transporteuradd.as_view(), name='transporteuradd'),
    path('transporteur/modify/', views.transporteurmodify.as_view(), name='transporteurmodify'),
    path('modify_trans/', views.transporteurmodify.modify),
    path('right_trans/', views.transporteurmodify.right),
    path('left_trans/', views.transporteurmodify.left),
    path('create_trans/', views.create_trans),
    path('delete_trans/', views.delete_trans),

    path('destinataire', views.destinataire.as_view(), name='destinataire'),
    path('destinataire/modify', views.destinatairemodify.as_view(), name='destinatairemodify'),
    path('right_destinataire/', views.destinatairemodify.right),
    path('left_destinataire/', views.destinatairemodify.left),

    path('destinataire/add', views.destinataireadd.as_view(), name='destinataireadd'),
    path('modify_dest/', views.destinatairemodify.modify, name='destinatairemodifysave'),
    path('create_dest/', views.destinataireadd.create),
    path('delete_dest/', views.destinataire.delete),

    path('client', views.client.as_view(), name='client'),
    path('client/add', views.clientadd.as_view(), name='clientadd'),
    path('create_cli/', views.clientadd.create),
    path('fill_contact/', views.clientadd.fill_contact), #nécessaire car les contacts sont dynamique
    path('delete_cli/', views.client.delete),
    path('client/modify', views.clientmodify.as_view(), name='clientmodify'),
    path('right_client/', views.clientmodify.right),
    path('left_client/', views.clientmodify.left),
    path('modify_cli/', views.clientmodify.modify, name='clientmodifysave'),
    path('modify_cli_contact/', views.clientmodify.modify_cli_contact, name='clientmodifysavecontact'),
    path('delete_cli_contact/', views.clientmodify.delete_cli_contact, name='clientmodifydeletecontact'),

    path('colis', views.colis.as_view(), name='colis'),
    path('colis/add', views.colisadd.as_view(), name='colisadd'),

    path('umentree', views.ume.as_view(), name='unitemanutentionentree'),
    path('umentree/reference', views.umereference.as_view(), name='unitemanutentionentreereference'),
    path('umentree/add', views.umeadd.as_view(), name='unitemanutentionentreeadd'),
    path('umentree/modify/', views.umemodify.as_view(), name='unitemanutentionentreemodify'),
    path('modify_ume/', views.umemodify.modify),
    path('ligneume/create/', views.umemodify.createligne),
    path('ume/col/print/', views.umemodify.printer),
    path('ume/delete_col/', views.umemodify.delete_colis),
    path('ume/delieums/', views.umemodify.delieums),
    path('create_ume/', views.umeadd.create),
    path('delete_ume/', views.ume.delete),
    path('sort_cols/', views.sortcolis), #appel l'algo qui va trier les "colis" pour les sortir dans les lbcs
    path('ume/sortOnecolis/', views.sortOnecolis), #appel l'algo qui va trier un seul "coli" pour le sortir dans les lbcs

    path('umsortie', views.ums.as_view(), name='unitemanutentionsortie'),
    path('umsortie/add', views.umsadd.as_view(), name='unitemanutentionsortieadd'),
    path('umsortie/modify/', views.umsmodify.as_view(), name='unitemanutentionsortiemodify'),
    path('modify_ums/', views.umsmodify.modify),
    path('ligneums/create/', views.umsmodify.createligne),
    path('ums/delete_col/', views.umsmodify.delete_colis),
    path('create_ums/', views.umsadd.create),
    path('delete_ums/', views.ums.delete),
    path('umsortie/modify/dateouverture/', views.umsmodify.dateouverture),
    path('umsortie/modify/datefermeture/', views.umsmodify.datefermeture),
    path('umsortie/modify/dateexpedition/', views.umsmodify.dateexpedition),

    #path('bon/add/<int:month>/', views.),
    path('etiquetteUMe/', views.etiquetteume.as_view(), name='etiquetteUMe'),
    path('etiquetteUMe/colis', views.etiquetteumecolis.as_view(), name='etiquetteUMecol'),
    path('etiquetteUMs/', views.etiquetteums.as_view(), name='etiquetteUMs'),
    path('etiquetteUMs/colissage/', views.etiquetteumscolissage.as_view(), name='etiquetteUMscolissage'),
]
