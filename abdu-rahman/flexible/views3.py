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

@method_decorator([login_required, transporteur_required], name='dispatch')
class IndexTView(ListView):
    
    context_object_name = 'tarifs'
    template_name = 'flexible/multiT.html'
    
    
    def get_queryset(self):
        
        queryset = TarifTransport.objects.filter(transporteur_id=self.request.user.transporteur)
        return queryset
   
  
    def get_context_data(self, **kwargs):


        if self.request.method == 'GET' and 'search' in self.request.GET:
            recherche2 =  self.request.GET.get('search') 
        else :
            recherche2 =  'rien'
        
        lesEntrepots =Entrepot.objects.filter(designation__icontains=recherche2) 
        lesPartenaires = User.objects.filter( is_partenaire=True ,nom__icontains=recherche2 ) 
        lesTransporteurs = User.objects.filter( is_transporteur=True , nom__icontains=recherche2) 


        
        rapportDepassement = timezone.now().date() - timedelta(days=10)
        rapportDepassement2 = timezone.now().date() - timedelta(days=1)
        
        
        results = chain(lesEntrepots)
        autres = chain( lesPartenaires, lesTransporteurs)
        context = super(IndexTView, self).get_context_data(**kwargs)
        context['entrepots'] = Entrepot.objects.all()
        context['places'] = Place.objects.all()
        context['entrepotsRecherche'] = results
        context['autres'] = autres
        context['tarifsT'] = TarifTransport.objects.filter(transporteur_id=self.request.user.transporteur)
        context['reponses'] = AcceptationCommandeLivraison.objects.filter(transporteur_id=self.request.user.transporteur)
        context['messagesT'] = Message.objects.filter(user_id=self.request.user)
        context['offresT'] = OffreCommandeLivraison.objects.filter(transporteur_id=self.request.user.transporteur,date__gte=rapportDepassement)
        context['today']  =  datetime.now()
        context['taches']  =AcceptationCommandeLivraison.objects.filter(transporteur_id=self.request.user.transporteur,is_accepted=True,Date__gte=rapportDepassement2)
        

        return context

@method_decorator([login_required, transporteur_required], name='dispatch')
class TarifVoyageur(ListView):
    
    context_object_name = 'tarifs'
    template_name = 'flexible/tarifTrans.html'
    
    
    def get_queryset(self):
        
        queryset = TarifTransport.objects.filter(transporteur_id=self.request.user.transporteur)
        return queryset
   
  
    def get_context_data(self, **kwargs):


        if self.request.method == 'GET' and 'search' in self.request.GET:
            recherche2 =  self.request.GET.get('search') 
        else :
            recherche2 =  'rien'
        
        lesEntrepots =Entrepot.objects.filter(designation__icontains=recherche2) 
        lesPartenaires = User.objects.filter( is_partenaire=True ,nom__icontains=recherche2 ) 
        lesTransporteurs = User.objects.filter( is_transporteur=True , nom__icontains=recherche2) 
        
        
        
        
        results = chain(lesEntrepots)
        autres = chain( lesPartenaires, lesTransporteurs)
        context = super(TarifVoyageur, self).get_context_data(**kwargs)
      
        context['places'] = Place.objects.all()
        context['entrepotsRecherche'] = results
        context['autres'] = autres
        context['messagesT'] = Message.objects.filter(user_id=self.request.user)
        context['offresT'] = OffreCommandeLivraison.objects.filter(transporteur_id=self.request.user.transporteur)

        return context


@method_decorator([login_required, transporteur_required], name='dispatch')
class TarifTransporteurCreate(CreateView):
    model = TarifTransport
    fields = ('designation', 'depart', 'arrive', 'nb_palettes','categorie','prix')
    template_name = 'flexible/ajoutTarifT.html'

  
    
    def form_valid(self, form):
        form.instance.transporteur = self.request.user.transporteur
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('tariftranspo')
        



@method_decorator([login_required, transporteur_required], name='dispatch')
class CamionsView(ListView):
    
    context_object_name = 'camions'
    template_name = 'flexible/camion.html'
    
    
    def get_queryset(self):
        
        queryset = Camion.objects.filter(transporteur_id=self.request.user.transporteur)
        return queryset
   
  
    def get_context_data(self, **kwargs):


        if self.request.method == 'GET' and 'search' in self.request.GET:
            recherche2 =  self.request.GET.get('search') 
        else :
            recherche2 =  'rien'
        
        lesEntrepots =Entrepot.objects.filter(designation__icontains=recherche2) 
        lesPartenaires = User.objects.filter( is_partenaire=True ,nom__icontains=recherche2 ) 
        lesTransporteurs = User.objects.filter( is_transporteur=True , nom__icontains=recherche2) 
        rapportDepassement2 = timezone.now().date() - timedelta(days=1)

        
        
        
        results = chain(lesEntrepots)
        autres = chain( lesPartenaires, lesTransporteurs)
        context = super(CamionsView, self).get_context_data(**kwargs)
        context['entrepots'] = Entrepot.objects.all()
        context['places'] = Place.objects.all()
        context['entrepotsRecherche'] = results
        context['autres'] = autres
        context['trajets'] = Trajet.objects.filter(camion__transporteur_id=self.request.user.transporteur)
        context['messagesT'] = Message.objects.filter(user_id=self.request.user)
        context['offresT'] = OffreCommandeLivraison.objects.filter(transporteur_id=self.request.user.transporteur)
        context['taches']  =AcceptationCommandeLivraison.objects.filter(transporteur_id=self.request.user.transporteur,is_accepted=True,Date__gte=rapportDepassement2)
        
        return context




@method_decorator([login_required, transporteur_required], name='dispatch')
class ReponseViewTransporteur(CreateView):
    model = AcceptationCommandeLivraison
    fields =('commentaire',  'client','offre','is_accepted')
   
    template_name = 'flexible/add_ResponseT.html'
    def get_form(self, *args, **kwargs):
        
        form = super(ReponseViewTransporteur, self).get_form(*args, **kwargs)
        rapportDepassement = timezone.now().date() - timedelta(days=1,hours=12)
        form.fields['client'].queryset= Client.objects.filter(transporteurs=self.request.user.transporteur).distinct()
        form.fields['offre'].queryset = OffreCommandeLivraison.objects.filter(transporteur_id=self.request.user.transporteur,date__gte=rapportDepassement)
        return form
    
    def form_valid(self, form):
        
        if not form.instance.client == form.instance.offre.client :
            print("")
            return redirect('repondreT')
        else :
            form.instance.transporteur = self.request.user.transporteur
            responseLivrasion = form.save(commit=False)

            responseLivrasion.save()
   
        return redirect('multiT')
