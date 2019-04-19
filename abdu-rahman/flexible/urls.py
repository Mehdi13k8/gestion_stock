
from django.urls import path
from django.conf.urls import  url, include
from django.views.generic import ListView
from .models import Entrepot,Client
from djgeojson.views import GeoJSONLayerView

from . import views,views1,views2,views3


urlpatterns = [

    path('compte/', include('django.contrib.auth.urls')),
    path('compte/signup/', views.SignUpView.as_view(), name='signup'),
    path('compte/signup/client/', views.ClientSignUpView.as_view(), name='client_signup'),
    path('compte/signup/testclient/', views.ClientTestSignUpView.as_view(), name='clientTest_signup'),
    path('offre/testclient/', views.OffreTestCreateView.as_view(), name='OffreTest_create'),
    
    path('compte/login/', views.logiin, name='login'),
    path('deconnexion', views.deconnexion, name='logout'),
    path('chose/', views.chosing, name='chosee'),
    path('add/', views.add, name='addd'),
    path('Process/', views.process, name='process'),

    path('compte/signup/client/', views.ClientSignUpView.as_view(), name='client_signup'),
    path('compte/signup/transporteur/', views.TransporteurSignUpView.as_view(), name='transporteur_signup'),
    path('compte/signup/partenaire/', views.PartenaireSignUpView.as_view(), name='partenaire_signup'),


    #path('', views.OffreListView.as_view(), name='home'),
    
    #path('search', views.search, name='search'),


    path('partenaire/', views.OffrePListView.as_view(), name='offreListP'),
    path('client/', views.OffreListView.as_view(), name='offreList'),
    path('client/infos', views.AllEntrepotsListView.as_view(), name='entrepotInfo'),
    
    
    path('', views.logiin, name='home'),
    
    
    
    path('client/reponses', views.ReponseView.as_view(), name='reponsesClient'),
    #path('offre/<int:pk>', views.OffreUpdateView.as_view(), name='nouvelleOffre'),
    #path('offre/ajout/', views.OffreCreateView.as_view(), name='offre_ajout'),
    path('chart/', views.chart, name='chart'),
    
    path('client/qualite/', views.AppreciationsCreateView.as_view(), name='uneAppreciation'),

    path('client/show/', views.BaseView.as_view(), name='show'),
    
    path('partenaire/show', views.BaseViewP.as_view(), name='showP'),
    path('appreciations/', views.AppreciationsListView.as_view(), name='appreciations'),

    path('schedules/', views.multicreate, name='schedules'),
    
    
    path('ajax/validate_username',views.validate_username, name='validate_username'),
    

    path('client/accueil', views1.IndexViewC.as_view(), name='multiC'),
    path('client/tarifs', views1.TarifsClient.as_view(), name='tarifC'),
    
    path('client/offre/<int:pk>', views1.OffreUpdateView.as_view(), name='nouvelleOffre'),
    path('client/offreTran/<int:pk>', views1.OffreTUpdateView.as_view(), name='nouvelleOffreT'),
    path('client/offreL/ajout', views1.OffreLCreateView.as_view(), name='offreL_ajout'),
    path('client/offreT/ajout', views1.OffreTCreateView.as_view(), name='offreT_ajout'),
    path('client/offreLivraion/ajout', views1.OffreLivraisonCreateView.as_view(), name='offreLiv_ajout'),
    path('client/offreTranspot/ajout', views1.OffreTransportCreateView.as_view(), name='offretra_ajout'),
    path('client/offre/<int:pk>', views1.OffreUpdateView.as_view(), name='nouvelleOffre'),


   
    path('client/produits', views1.ProduitsClient.as_view(), name='mesProduits'),
    path('client/produits/ajout/', views1.ProduitCreateView.as_view(), name='produit_ajout'),


    path('partenaire/accueil', views2.IndexView.as_view(), name='multi'),
    path('partenaire/entrepots/', views2.EntrepotPartenaire.as_view(), name='mesEntrepots'),
    path('partenaire/entrepots/ajout/', views2.EntrepotCreateView.as_view(), name='entrepot_ajout'),
    path('partenaire/entrepots/place-ajout/', views2.PlaceCreateView.as_view(), name='place_ajout'),
    path('partenaire/entrepot/<int:pk>/places/', views2.PlaceAllView.as_view(), name='lesplaces'),
    path('partenaire/entrepot/place/<int:pk>/', views2.PlaceProductView.as_view(), name='placerProduit'),
    path('partenaire/tarifs/', views2.TarifPartenaire.as_view(), name='tarifPart'),
    path('partenaire/tarifs/ajout', views2.TarifCreateView.as_view(), name='tarif_ajout'),
    path('partenaire/tarifs/<int:pk>/', views2.TarifModifyView.as_view(), name='modifyTarif'),
    path('partenaire/repondre', views2.ReponseViewPartenaire.as_view(), name='reponses'),
    path('partenaire/reponse/<int:pk>/', views2.ReponseViewPartenaireP.as_view(), name='repond'),

    path('transporteur/accueil/', views3.IndexTView.as_view(), name='multiT'),
    path('transporteur/tarifs/', views3.TarifVoyageur.as_view(), name='tariftranspo'),
    path('transporteur/tarifs/ajout/', views3.TarifTransporteurCreate.as_view(), name='tarifT_ajout'),
    path('transporteur/camions/', views3.CamionsView.as_view(), name='camions'),
    path('transporteur/repondre/ajout/', views3.ReponseViewTransporteur.as_view(), name='repondreT'),

    path('geo/', views.Home.as_view(), name='geodata'),
    path('datas/', views.points_view, name='points'),
    path('', views.MainPageView.as_view(), name='map'),

    path('geo/geojson', GeoJSONLayerView.as_view(model=Entrepot, properties=('designation', 'adresse', 'capacite')), name='data')
   
   
   
] 

