from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import ListView

urlpatterns = [
    path('', views.index.as_view(), name='index'),

    #path('accounts/login/', auth_views.LoginView.as_view()),
    path('login/', views.index_login.as_view(), name='login'),

    path('index', views.index.as_view()),

    path('bon_entree', views.BonCommandeEntree_index.as_view(), name='bonCommandeEntree'), #page des bon de commande entree
    path('bon_entree/add', views.BonCommandeEntreeadd.as_view(), name='bonCommandeEntreeadd'), #page des possibilité a ajouter au bon de commande entree
    path('bon_entree/adding/', views.BonCommandeEntreeadd.add), #fonction 'add' dans la view qui permet de "crée" dans la bdd l'objet

    path('bon_entree/modify', views.BonCommandeEntreemodify.as_view(), name='bonCommandeEntreemodify'),
    path('delete_bon_entree/', views.BonCommandeEntree_index.delete),

    path('bon', views.ListeArticles.as_view(), name='bonCommandeSortie'),
    path('bon/add', views.bonCommandeSortieadd, name ='bonCommandeSortieadd'),


    path('bonLivraisonsortie', views.bonLivraisonSortie.as_view(), name='bonLivraisonSortie'),
    path('bonLivraisonsortie/add', views.bonLivraisonSortieadd.as_view(), name='bonLivraisonSortieadd'),

    path('bonLivraisonentree', views.bonLivraisonEntree.as_view(), name='bonLivraisonEntree'),
    path('bonLivraisonentree/add', views.bonLivraisonEntreeadd.as_view(), name='bonLivraisonEntreeadd'),
    path('bonLivraisonentree/modify', views.bonLivraisonEntreeadd.as_view(), name='bonLivraisonEntreemodify'),
    path('ble/delete/', views.bonLivraisonEntree.delete),
    path('ble/create/', views.bonLivraisonEntreeadd.create),

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
    path('modify_trans/', views.transporteurmodify.modify, name='transporteurmodifysave'),
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

    path('umentree', views.ume.as_view(), name='unitemanutentionentree'),
    path('umentree/add', views.umeadd.as_view(), name='unitemanutentionentreeadd'),
    path('umentree/modify/', views.umemodify.as_view(), name='unitemanutentionentreemodify'),
    path('modify_ume/', views.umemodify.modify, name='transporteurmodifysave'),
    path('create_ume/', views.umeadd.create),
    path('delete_ume/', views.ume.delete),

    #path('bon/add/<int:month>/', views.),
]