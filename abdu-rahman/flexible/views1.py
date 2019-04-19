from django.http import HttpResponse, Http404,HttpResponseRedirect
from datetime import datetime
from django.db.models import Avg, Count
from django.shortcuts import render, redirect,  get_object_or_404,render_to_response
from flexible.models import Client
from .forms import ClientSignUpForm, PartenaireSignUpForm, ConnexionForm,TransporteurSignUpForm
from django.views.generic import ListView, DetailView,UpdateView
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import CreateView,View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.db.models import F

from django.contrib.auth.decorators import login_required
from .decorators import client_required,partenaire_required,transporteur_required
from .fusioncharts import FusionCharts
from .models import chose
from .models import OffreL,OffreT,User,Client,Produit,Trajet,Message,SuiviStock,SuiviTransporteur,Camion,AcceptationCommandeLivraison,OffreCommandeLivraison,Tarif,TarifTransport,Transporteur,Appreciation,Partenaire,Entrepot,Place,OffreLivraison,AcceptationLivraison

from django.core.serializers import serialize

from itertools import chain
#geolocalisation des user

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q
from django.template.context_processors import csrf
from .forms import ChoseForm,ClientTestSignUpForm
from datetime import timedelta
from django.utils import timezone

 
'''
#coordonnee de crossdock a Cavaillon
longitude = 5.07029

latitude = 43.840971
user_location = Point(longitude, latitude, srid=4326)
'''

#plus la peine de recuperer les coordonnees
@method_decorator([login_required, client_required], name='dispatch')
class IndexViewC(ListView):
    
    context_object_name = 'homeC'    
    template_name = 'flexible/multiC.html'
  
   
      
 
    def get_queryset(self):
        queryset = OffreLivraison.objects.filter(client_id=self.request.user.client)
        return queryset

    def get_context_data(self, **kwargs):

        recherche='rien'

        u=User.objects.get(username=self.request.user) 

        if self.request.method == 'GET'and self.request.GET.get('search')!= '' and 'search' in self.request.GET:
            recherche =  self.request.GET.get('search')
            

        elif self.request.GET.get('search')== '':
            recherche ='rien'

        lesEntrepots = Entrepot.objects.filter(designation__icontains=recherche) 
        lesPartenaires = User.objects.filter( is_partenaire=True ,nom__icontains=recherche ) 
        lesTransporteurs = User.objects.filter( is_transporteur=True , nom__icontains=recherche) 
        lesLivraisonsD = TarifTransport.objects.filter( depart__icontains=recherche)
        lesLivraisonsA = TarifTransport.objects.filter(  arrive__icontains=recherche)
        

        
        
        
        
        results = chain(lesEntrepots)
        autres = chain( lesPartenaires, lesTransporteurs)
        destinations = chain( lesLivraisonsD, lesLivraisonsA)

        context = super(IndexViewC, self).get_context_data(**kwargs)
        
        #afficher les entrepots et transporteurs proches du client
        #si l'admin ne nus a pas encore attribué de coordonnée gps on ne les verra  pas :)
        if not self.request.user.client.user.coordonnee== None:
            context['entsProches'] =  Entrepot.objects.annotate(distance=Distance("geom", u.coordonnee)).order_by("distance")[0:5]
            context['transProches'] =  Transporteur.objects.annotate(distance=Distance("user__coordonnee", u.coordonnee)).order_by("distance")[0:5]
        
        context['messages'] = Message.objects.filter(user_id=self.request.user)
        context['partenaires'] = Partenaire.objects.all()
        context['entrepots'] = results
        context['autres'] = autres
        context['departs'] = destinations
        context['reponses'] = AcceptationLivraison.objects.filter(client_id=self.request.user.client)
        context['produits'] = Produit.objects.filter(clientProp_id=self.request.user.client)
        context['tarifs'] = Tarif.objects.all().annotate(prixFinal=F('prix') + F('prix')*0.3).order_by('nb_palettes','categorie','prixFinal')
        context['tarifsT'] = TarifTransport.objects.all().annotate(prixFinalT=F('prix') + F('prix')*0.08).order_by('nb_palettes','categorie','prixFinalT')
        context['offresT'] = OffreCommandeLivraison.objects.filter(client_id=self.request.user.client)
        context['reponsesT'] = AcceptationCommandeLivraison.objects.filter(client_id=self.request.user.client)
        context['calcul']=OffreLivraison.objects.all().values('partenaire__user__nom').annotate(c=Count('partenaire')).order_by('-c')[0:3]
        context['calcul3']=OffreLivraison.objects.all().values('entrepot__designation').annotate(c=Count('entrepot')).order_by('-c')[0:3]
        context['calcul2']=OffreCommandeLivraison.objects.all().values('transporteur__user__nom').annotate(c=Count('transporteur')).order_by('-c')[0:3]
        return context



@method_decorator([login_required, client_required], name='dispatch')
class TarifsClient(ListView):
    
    context_object_name = 'homeC'    
    template_name = 'flexible/tarifC.html'
  
   
      
 
    def get_queryset(self):
        queryset = OffreLivraison.objects.filter(client_id=self.request.user.client)
        return queryset

    def get_context_data(self, **kwargs):

        recherche='rien'

        u=User.objects.get(username=self.request.user) 

        if self.request.method == 'GET'and self.request.GET.get('search')!= '' and 'search' in self.request.GET:
            recherche =  self.request.GET.get('search')
            

        elif self.request.GET.get('search')== '':
            recherche ='rien'

        lesEntrepots =Entrepot.objects.filter(designation__icontains=recherche) 
        lesPartenaires = User.objects.filter( is_partenaire=True ,nom__icontains=recherche ) 
        lesTransporteurs = User.objects.filter( is_transporteur=True , nom__icontains=recherche) 
        lesLivraisonsD = TarifTransport.objects.filter( depart__icontains=recherche)
        lesLivraisonsA = TarifTransport.objects.filter(  arrive__icontains=recherche)
        

        
        
        
        
        results = chain(lesEntrepots)
        autres = chain( lesPartenaires, lesTransporteurs)
        destinations = chain( lesLivraisonsD, lesLivraisonsA)

        context = super(TarifsClient, self).get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(user_id=self.request.user)
        context['partenaires'] = Partenaire.objects.all()
        context['entrepots'] = results
        context['autres'] = autres
        context['departs'] = destinations
        context['produits'] = Produit.objects.filter(clientProp_id=self.request.user.client)
        context['tarifs'] = Tarif.objects.all().annotate(prixFinal=F('prix') + F('prix')*0.3).order_by('nb_palettes','categorie','prixFinal')
        context['tarifsT'] = TarifTransport.objects.all().annotate(prixFinalT=F('prix') + F('prix')*0.08).order_by('nb_palettes','categorie','prixFinalT')
        context['offresT'] = OffreCommandeLivraison.objects.filter(client_id=self.request.user.client)
        context['reponsesT'] = AcceptationCommandeLivraison.objects.filter(client_id=self.request.user.client)
        return context


@method_decorator([login_required, client_required], name='dispatch')
class OffreUpdateView(UpdateView):
    model = OffreLivraison
    fields = ('partenaire', 'entrepot', 'offre')
    context_object_name = 'monoffre'
    template_name = 'flexible/offre_change_form.html' 

    
    def get_queryset(self):
        
        queryset = OffreLivraison.objects.filter(id=self.kwargs['pk'])
        return queryset
    
    def get_success_url(self):
        return reverse('multiC')



@method_decorator([login_required, client_required], name='dispatch')
class OffreTUpdateView(UpdateView):
    model = OffreCommandeLivraison
    fields = ('designation', 'offre', 'transporteur')
    context_object_name = 'monoffre'
    template_name = 'flexible/offre_change_form.html' 

    
    def get_queryset(self):
        
        queryset = OffreCommandeLivraison.objects.filter(id=self.kwargs['pk'])
        return queryset
    
    def get_success_url(self):
        return reverse('multiC')



@method_decorator([login_required, client_required], name='dispatch')
class OffreLCreateView(CreateView):
    model = OffreL
    fields = ('designation', 'quantité', 'produit', 'categorie', 'datearrive')
    template_name = 'flexible/ajoutOffre.html'
    context_object_name = 'mesoffres'
    def get_form(self, *args, **kwargs):
        
        form = super(OffreLCreateView, self).get_form(*args, **kwargs)
       
        form.fields['produit'].queryset= Produit.objects.filter(clientProp=self.request.user.client)
       
        return form
    
    def form_valid(self, form):
        form.instance.client = self.request.user.client
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('offreLiv_ajout')




@method_decorator([login_required, client_required], name='dispatch')
class OffreTCreateView(CreateView):
    model = OffreT
    fields = ('designation', 'quantité', 'produit', 'categorie', 'depart', 'arrive', 'adresse', 'adresse2', 'livraison', 'enlevement', 'datearrive')
    template_name = 'flexible/ajoutOffreT.html'

    def form_valid(self, form):
        form.instance.client = self.request.user.client
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('offretra_ajout')


@method_decorator([login_required, client_required], name='dispatch')
class OffreLivraisonCreateView(CreateView):
    model = OffreLivraison
    fields = ('partenaire', 'entrepot', 'offre')
    template_name = 'flexible/ajoutOffre.html'
    
    

    def get_form(self, *args, **kwargs ):
        if self.request.method == 'GET' and 'part' in self.request.GET:
            iteration =  self.request.GET.get('part').lower()
            
        else :
            iteration = "--"  
        form = super(OffreLivraisonCreateView, self).get_form(*args, **kwargs)
        form.fields['partenaire'].queryset = Partenaire.objects.filter(user__nom=iteration)
        form.fields['offre'].queryset = OffreL.objects.filter(client_id=self.request.user.client)
        form.fields['entrepot'].queryset = Entrepot.objects.filter(partenaireProp__user__nom=iteration)
        
        

        return form
    def form_valid(self, form):
        form.instance.client = self.request.user.client
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('nouvelleOffre', offre.pk)



@method_decorator([login_required, client_required], name='dispatch')
class OffreTransportCreateView(CreateView):
    model = OffreCommandeLivraison
    fields = ('designation','transporteur' ,'offre')
    template_name = 'flexible/ajoutOffreT.html'

    def get_form(self, *args, **kwargs):


        form = super(OffreTransportCreateView, self).get_form(*args, **kwargs)
        form.fields['offre'].queryset = OffreT.objects.filter(client_id=self.request.user.client)
        return form
    def form_valid(self, form):
        form.instance.client = self.request.user.client
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('nouvelleOffreT', offre.pk)





@method_decorator([login_required, client_required], name='dispatch')
class ProduitsClient(ListView):
    
    context_object_name = 'homeC'    
    template_name = 'flexible/produits.html'
  
   
      
 
    def get_queryset(self):
        queryset = OffreLivraison.objects.filter(client_id=self.request.user.client)
        return queryset

    def get_context_data(self, **kwargs):

        recherche='rien'

        u=User.objects.get(username=self.request.user) 


        if self.request.method == 'GET'and self.request.GET.get('search')!= '' and 'search' in self.request.GET:
            recherche =  self.request.GET.get('search')
            

        elif self.request.GET.get('search')== '':
            recherche ='rien'

        lesEntrepots =Entrepot.objects.filter(designation__icontains=recherche) 
        lesPartenaires = User.objects.filter( is_partenaire=True ,nom__icontains=recherche ) 
        lesTransporteurs = User.objects.filter( is_transporteur=True , nom__icontains=recherche) 
        lesLivraisonsD = TarifTransport.objects.filter( depart__icontains=recherche)
        lesLivraisonsA = TarifTransport.objects.filter(  arrive__icontains=recherche)
        

        
        
        
        
        results = chain(lesEntrepots)
        autres = chain( lesPartenaires, lesTransporteurs)
        destinations = chain( lesLivraisonsD, lesLivraisonsA)

        context = super(ProduitsClient, self).get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(user_id=self.request.user)
        context['partenaires'] = Partenaire.objects.all()
        context['entrepots'] = results
        context['autres'] = autres
        context['departs'] = destinations
        context['produits'] = Produit.objects.filter(clientProp_id=self.request.user.client)
        context['tarifs'] = Tarif.objects.all().annotate(prixFinal=F('prix') + F('prix')*0.3).order_by('nb_palettes','categorie','prixFinal')
        context['tarifsT'] = TarifTransport.objects.all().annotate(prixFinal=F('prix') + F('prix')*0.3).order_by('nb_palettes','categorie','prixFinal')
        context['offresT'] = OffreCommandeLivraison.objects.filter(client_id=self.request.user.client)
        context['reponsesT'] = AcceptationCommandeLivraison.objects.filter(client_id=self.request.user.client)
        return context


@method_decorator([login_required, client_required], name='dispatch')
class ProduitCreateView(CreateView):
    model = Produit
    fields = ('designation', 'refproduit', 'categorie','photo')
    template_name = 'flexible/ajoutProd.html'

    def form_valid(self, form):
        form.instance.clientProp = self.request.user.client
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('mesProduits')