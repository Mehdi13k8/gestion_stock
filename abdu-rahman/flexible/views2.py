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
@method_decorator([login_required, partenaire_required], name='dispatch')
class IndexView(ListView):
    context_object_name = 'offres'    
    template_name = 'flexible/multi.html'

    
    #objects.filter(added__gte=past_week)
    
    def get_queryset(self):
        rapportDepassement = timezone.now().date() - timedelta(days=10)
        #queryset = OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire)
        #gte=plus grand ou egal à #lte
        queryset = OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire,Date__gte=rapportDepassement)
        return queryset

       
    def get_context_data(self, **kwargs):
        rapportDepassement2 = timezone.now().date() - timedelta(days=1)
        if self.request.method == 'GET' and 'search' in self.request.GET:
            recherche2 =  self.request.GET.get('search') 
        else :
            recherche2 =  'rien'
        
        lesEntrepots =Entrepot.objects.filter(designation__icontains=recherche2) 
        lesPartenaires = User.objects.filter( is_partenaire=True ,nom__icontains=recherche2 ) 
        lesTransporteurs = User.objects.filter( is_transporteur=True , nom__icontains=recherche2) 
        
        
        
        results = chain(lesEntrepots)
        autres = chain( lesPartenaires, lesTransporteurs)


        context = super(IndexView, self).get_context_data(**kwargs)
        context['entrepots'] = Entrepot.objects.filter(partenaireProp_id=self.request.user.partenaire)
        context['prods'] = Produit.objects.all()
        context['places'] = Place.objects.all()
        context['entrepotsRecherche'] = results
        context['autres'] = autres
        context['reponses'] = AcceptationLivraison.objects.filter(partenaire_id=self.request.user.partenaire)
        context['suiviS'] = SuiviStock.objects.filter(entrepot__partenaireProp_id=self.request.user.partenaire)
        context['suiviT'] =  SuiviTransporteur.objects.filter(entrepot__partenaireProp_id=self.request.user.partenaire)
        context['OffresCommandes'] =  AcceptationCommandeLivraison.objects.all()
        context['appreciations'] = Appreciation.objects.all()
        context['tarifs'] = Tarif.objects.filter(entrepot__partenaireProp_id=self.request.user.partenaire)
        context['messages'] = Message.objects.filter(user_id=self.request.user)
        context['today']  =  datetime.now()
        context['taches']  =AcceptationLivraison.objects.filter(partenaire_id=self.request.user.partenaire,is_accepted=True,Date__gte=rapportDepassement2)
        context['calcul']=Place.objects.filter(partenaire_id=self.request.user.partenaire,refproduit__isnull=False).values('refproduit','entrepot').annotate(c=Count('refproduit')).order_by('-c')
        context['espace']=rapportDepassement2
        return context

@method_decorator([login_required, partenaire_required], name='dispatch')
class EntrepotPartenaire(ListView):
    context_object_name = 'homeP'    
    template_name = 'flexible/entrepots.html'


    def get_queryset(self):
        queryset = AcceptationLivraison.objects.filter(partenaire_id=self.request.user.partenaire)
        return queryset

    def get_context_data(self, **kwargs):
        rapportDepassement2 = timezone.now().date() - timedelta(days=1)
        
        if self.request.method == 'GET' and 'search' in self.request.GET:
            recherche2 =  self.request.GET.get('search') 
        else :
            recherche2 =  'rien'
        
        lesEntrepots =Entrepot.objects.filter(designation__icontains=recherche2) 
        lesPartenaires = User.objects.filter( is_partenaire=True ,nom__icontains=recherche2 ) 
        lesTransporteurs = User.objects.filter( is_transporteur=True , nom__icontains=recherche2) 
        
        
        results = chain(lesEntrepots)
        autres = chain( lesPartenaires, lesTransporteurs)

        context = super(EntrepotPartenaire, self).get_context_data(**kwargs)
        context['entrepots'] = Entrepot.objects.filter(partenaireProp_id=self.request.user.partenaire)
        context['places'] = Place.objects.filter(partenaire_id=self.request.user.partenaire)
        context['ents'] = Entrepot.objects.filter(partenaireProp_id=self.request.user.partenaire).prefetch_related('places')
        context['entrepotsRecherche'] = results
        context['autres'] = autres
        context['appreciations'] = Appreciation.objects.all()
        context['tarifs'] = Tarif.objects.filter(entrepot__partenaireProp_id=self.request.user.partenaire)
        context['messages'] = Message.objects.filter(user_id=self.request.user)
        context['taches']  =AcceptationLivraison.objects.filter(partenaire_id=self.request.user.partenaire,is_accepted=True,Date__gte=rapportDepassement2)
        context['calcul']=Place.objects.filter(partenaire_id=self.request.user.partenaire,refproduit__isnull=False).values('refproduit','entrepot__designation').annotate(c=Count('refproduit')).order_by('entrepot__designation')
       
        return context


@method_decorator([login_required, partenaire_required], name='dispatch')
class EntrepotCreateView(CreateView):
    model = Entrepot
    fields = ('designation', 'adresse', 'city', 'capacite', 'specificite','photo')
    template_name = 'flexible/ajoutEntrepot.html'

    def form_valid(self, form):
        form.instance.partenaireProp = self.request.user.partenaire
        
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('mesEntrepots')


@method_decorator([login_required, partenaire_required], name='dispatch')
class PlaceCreateView(CreateView):
    model = Place
    fields = ('designation', 'entrepot' ,'refproduit','destinataire', 'categorie','nb_palettes','state')
    template_name = 'flexible/ajoutPlace.html'
   
    
    #filtrer le formulaire au niveau des foreignKEy
    def get_form(self, *args, **kwargs):
        form = super(PlaceCreateView, self).get_form(*args, **kwargs)
        form.fields['entrepot'].queryset = Entrepot.objects.filter(partenaireProp_id=self.request.user.partenaire)

        return form
    
    def form_valid(self, form):

        
        if self.request.method == 'POST' and 'add' in self.request.GET:
            iteration =  int(self.request.GET.get('add'))
        else :
            iteration = 1


        i=1
        for i in range(iteration):
            form.instance.partenaire = self.request.user.partenaire
            #Saving with commit=False gets you a model object, then you can add your extra data and save it.
            offre = form.save(commit=False)
            offre.pk = None
            i+=1
            offre.save() 

       
        return redirect('mesEntrepots')
    

@method_decorator([login_required, partenaire_required], name='dispatch')
class PlaceAllView(ListView):
    model = Place
   
    context_object_name = 'mesplaces'
    template_name = 'flexible/allplaces.html'

    def get_queryset(self):
        queryset = Place.objects.all()
        return queryset


@method_decorator([login_required, partenaire_required], name='dispatch')
class PlaceProductView(UpdateView):
    model = Place
    fields = '__all__' 
    
    template_name = 'flexible/placeModify.html'

    
    def get_queryset(self):
        
        queryset = Place.objects.filter(id=self.kwargs['pk'])
        return queryset
    
    def get_success_url(self):
        return reverse('mesEntrepots')

@method_decorator([login_required, partenaire_required], name='dispatch')
class TarifPartenaire(ListView):
    context_object_name = 'homeP'    
    template_name = 'flexible/tarifPart.html'


    
    def get_queryset(self):
        queryset = AcceptationLivraison.objects.filter(partenaire_id=self.request.user.partenaire)
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


        context = super(TarifPartenaire, self).get_context_data(**kwargs)
        context['entrepots'] = Entrepot.objects.filter(partenaireProp_id=self.request.user.partenaire)
        context['places'] = Place.objects.filter(partenaire_id=self.request.user.partenaire)
        context['entrepotsRecherche'] = results
        context['autres'] = autres
        context['appreciations'] = Appreciation.objects.all()
        context['tarifs'] = Tarif.objects.filter(entrepot__partenaireProp_id=self.request.user.partenaire)
        context['messages'] = Message.objects.filter(user_id=self.request.user)


       
        return context

@method_decorator([login_required, partenaire_required], name='dispatch')
class TarifCreateView(CreateView):
    model = Tarif
    fields = ('designation', 'entrepot', 'categorie', 'nb_palettes','prix')
    template_name = 'flexible/ajoutTarifP.html'

    def get_form(self, *args, **kwargs):
        form = super(TarifCreateView, self).get_form(*args, **kwargs)
        form.fields['entrepot'].queryset = Entrepot.objects.filter(partenaireProp_id=self.request.user.partenaire)
        return form
    
    def form_valid(self, form):
            
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('tarifPart')



@method_decorator([login_required, partenaire_required], name='dispatch')
class TarifModifyView(UpdateView):
    model = Tarif
    fields = '__all__' 
    
    template_name = 'flexible/tarifModify.html'

    
    def get_queryset(self):
        
        queryset = Tarif.objects.filter(id=self.kwargs['pk'])
        return queryset
    
    def get_success_url(self):
        return reverse('multi')


    
@method_decorator([login_required, partenaire_required], name='dispatch')
class ReponseViewPartenaire(CreateView):
    model = AcceptationLivraison
    fields =('commentaire',  'client','offre','is_accepted')
   
    template_name = 'flexible/add_response.html'
    def get_form(self, *args, **kwargs):
        
        form = super(ReponseViewPartenaire, self).get_form(*args, **kwargs)
        rapportDepassement = timezone.now().date() - timedelta(days=1,hours=12)
        #queryset = OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire)
        #gte=plus grand ou egal à #lte
        #queryset =OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire,Date__gte=past_week) 
        form.fields['client'].queryset= Client.objects.filter(crossdocker=self.request.user.partenaire).distinct()
        #form.fields['offre'].queryset = OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire)
        form.fields['offre'].queryset = OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire,Date__gte=rapportDepassement)
        return form
    
    def form_valid(self, form):
        
        if not form.instance.client == form.instance.offre.client :
            print("")
            return redirect('reponses')
        else :
            form.instance.partenaire = self.request.user.partenaire
            responseLivrasion = form.save(commit=False)

            responseLivrasion.save()
   
        return redirect('multi')

@method_decorator([login_required, partenaire_required], name='dispatch')
class ReponseViewPartenaireP(CreateView):
    model = AcceptationLivraison
    fields =('commentaire',  'client','offre','is_accepted')
   
    template_name = 'flexible/add_response.html'
    def get_form(self, *args, **kwargs):
        
        form = super(ReponseViewPartenaireP, self).get_form(*args, **kwargs)
        rapportDepassement = timezone.now().date() - timedelta(days=1,hours=12)
        #queryset = OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire)
        #gte=plus grand ou egal à #lte
        #queryset =OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire,Date__gte=past_week) 
        form.fields['client'].queryset= Client.objects.filter(crossdocker=self.request.user.partenaire).distinct()
        #form.fields['offre'].queryset = OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire)
        form.fields['offre'].queryset = OffreLivraison.objects.filter(id=self.kwargs['pk'],Date__gte=rapportDepassement)
        return form
    
    def form_valid(self, form):
        
        if not form.instance.client == form.instance.offre.client :
            print("")
            return redirect('repond')
        else :
            form.instance.partenaire = self.request.user.partenaire
            responseLivrasion = form.save(commit=False)

            responseLivrasion.save()
   
        return redirect('multi')