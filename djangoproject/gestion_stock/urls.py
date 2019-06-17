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

    path('modif_typefour/', views.modif_typef.as_view(), name='modif_typefour'),
    path('modif_typefour/save/', views.modif_typef.as_view(), name='modif_typefour_save'),

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
    path('delete_bon_sortie/', views.bonCommandeSortie.delete),

    path('uploadbc/', views.uploadbc),


    path('bonLivraisonsortie', views.bonLivraisonSortie.as_view(), name='bonLivraisonSortie'),
    path('bonLivraisonsortie/add', views.bonLivraisonSortieadd.as_view(), name='bonLivraisonSortieadd'),

    path('lettrevoitureentree', views.lettrevoitureentree.as_view(), name='lve'),
    path('lettrevoitureentree/modify', views.lettrevoitureentreemodify.as_view(), name='lvemodify'),
    path('lve/modify/', views.lettrevoitureentreemodify.modify),
    path('lve/modify/createbl/', views.lettrevoitureentreemodify.createbl),
    path('lettrevoitureentree/add', views.lettrevoitureentreeadd.as_view(), name='lveadd'),
    path('lve/create/', views.lettrevoitureentreeadd.create),
    path('lve/delete/', views.lettrevoitureentree.delete),

    path('bonLivraisonentree', views.bonLivraisonEntree.as_view(), name='bonLivraisonEntree'),
    path('bonLivraisonentree/add', views.bonLivraisonEntreeadd.as_view(), name='bonLivraisonEntreeadd'),
    path('bonLivraisonentree/modify', views.bonLivraisonentreemodify.as_view(), name='bonLivraisonEntreemodify'),
    path('right_ble/', views.bonLivraisonentreemodify.right),
    path('left_ble/', views.bonLivraisonentreemodify.left),
    path('ble/modify/', views.bonLivraisonentreemodify.modify),
    path('ble/delete/', views.bonLivraisonEntree.delete),
    path('ble/create/', views.bonLivraisonEntreeadd.create),
    path('ligneble/create/', views.bonLivraisonEntreeadd.createligne),
    path('ligneble/delete/', views.bonLivraisonEntreeadd.deleteligne),


    path('article', views.article.as_view(), name='article'),
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
    path('umentree/add', views.umeadd.as_view(), name='unitemanutentionentreeadd'),
    path('umentree/modify/', views.umemodify.as_view(), name='unitemanutentionentreemodify'),
    path('modify_ume/', views.umemodify.modify),
    path('ligneume/create/', views.umemodify.createligne),
    path('ume/delete_col/', views.umemodify.delete_colis),
    path('create_ume/', views.umeadd.create),
    path('delete_ume/', views.ume.delete),

    path('umsortie', views.ums.as_view(), name='unitemanutentionsortie'),
    path('umsortie/add', views.umsadd.as_view(), name='unitemanutentionsortieadd'),
    path('umsortie/modify/', views.umsmodify.as_view(), name='unitemanutentionsortiemodify'),
    path('modify_ums/', views.umsmodify.modify),
    path('ligneums/create/', views.umsmodify.createligne),
    path('ums/delete_col/', views.umsmodify.delete_colis),
    path('create_ums/', views.umsadd.create),
    path('delete_ums/', views.ums.delete),

    #path('bon/add/<int:month>/', views.),
]
