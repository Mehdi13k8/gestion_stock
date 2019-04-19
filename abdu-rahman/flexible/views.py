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
from .forms import ChoseForm,ClientTestSignUpForm,ScheduleForm
from datetime import timedelta
from django.utils import timezone


from django.http import JsonResponse
 
'''
#coordonnee de crossdock a Cavaillon
longitude = 5.07029

latitude = 43.840971
user_location = Point(longitude, latitude, srid=4326)
'''

def multicreate(request):        
    if request.method == "POST":
        forms = [
            ScheduleForm(dict(name=n, date_from=df, date_to=dt, desc=ds))
            for n, df, dt, ds in zip(
                request.POST.getlist("name"),
                request.POST.getlist("date_from"),
                request.POST.getlist("date_to"),
                request.POST.getlist("desc"),
            )
        ]
        if all(forms[i].is_valid() for i in range(len(forms))):                
            for form in forms:
                form.save() 
            return HttpResponse(
                f"success to create {len(forms)} Schedule instances."
            )
    else:
        forms = [ScheduleForm() for _ in range(3)]
    return render(request, "flexible/schedule.html", {"forms": forms})
 
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def process(request):
    

    return render(request, 'flexible/baseProcess.html')

def chosing(request):
    args = {}
    args.update(csrf(request))
    args['chosee'] = chose.objects.all()

    return render_to_response('flexible/test.html', args)

def add(request):
    if request.POST:
        form = ChoseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return  redirect('addd')
    else:
        form = ChoseForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('flexible/add.html', args)

class ClientTestSignUpView(CreateView):
    model = User
    form_class = ClientTestSignUpForm
    template_name = 'flexible/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('addd')

class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'flexible/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('multiC')


def points_view(request):
    points_as_geojson = serialize('geojson', Client.objects.all())
    return HttpResponse(points_as_geojson, content_type='json')

class MainPageView(TemplateView):
    template_name = 'flexible/map.html'

class Home(ListView):
  
    model = User
    context_object_name = "users"
   
   

    def get_queryset(self):
        u=User.objects.get(username=self.request.user)
        
       
        
        queryset = User.objects.annotate(
        distance=Distance("coordonnee", u.coordonne)
        ).order_by("distance")[0:6]
        return queryset

    
    template_name = "flexible/map.html"


home = Home.as_view()





class TransporteurSignUpView(CreateView):
    model = User
    form_class = TransporteurSignUpForm
    template_name = 'flexible/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'transporteur'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('multiT')

class SignUpView(TemplateView): 
    template_name = 'flexible/signup.html'
    
    
    

  

def deconnexion(request):

    logout(request)

    return redirect(reverse('login')) 
def logiin(request):

    error = False


    if request.method == "POST":

        form = ConnexionForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes

            if user:  # Si l'objet renvoyé n'est pas None

                login(request, user)  # nous connectons l'utilisateur

            else: # sinon une erreur sera affichée

                error = True

    else:

        form = ConnexionForm()


    return render(request, 'registration/login.html', locals())




class PartenaireSignUpView(CreateView):
    model = User
    form_class = PartenaireSignUpForm
    template_name = 'flexible/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'partenaire'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('multi')

@method_decorator([login_required, partenaire_required], name='dispatch')
class OffrePListView(ListView):
    model = OffreLivraison

    ordering = ('Date', )
    context_object_name = 'offresP'
    template_name = 'flexible/offreListP.html'
   
    def get_queryset(self):
        queryset = OffreLivraison.objects.filter(partenaire_id=self.request.user.partenaire)
        return queryset

@method_decorator([login_required, partenaire_required], name='dispatch')
class EntrepotsListView(ListView):
    model = Entrepot

    context_object_name = 'depots'
    template_name = 'flexible/listeEntrepots.html'
   
    def get_queryset(self):
        queryset = Entrepot.objects.filter(partenaireProp_id=self.request.user.partenaire)
        return queryset
    
@method_decorator([login_required, client_required], name='dispatch')
class OffreListView(ListView):
    model = OffreLivraison
    ordering = ('Date', )
    context_object_name = 'offres'
    template_name = 'flexible/offreList.html'
   
    def get_queryset(self):
        queryset = OffreLivraison.objects.filter(client_id=self.request.user.client)
        return queryset

class OffreTestCreateView(CreateView):
    model = OffreLivraison
    fields = ('designation', 'quantité','categorie', 'datearrive')
    template_name = 'flexible/ajoutOffre.html'

    def form_valid(self, form):
        form.instance.client = Client.objects.filter(pk=1)
        form.instance.partenaire=Partenaire.objects.filter(pk=2)
        form.instance.entrepot=Entrepot.objects.filter(designation="font08")
        form.instance.produit=Produit.objects.filter(designation="gateau sucré")
        
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('addd')    


@method_decorator([login_required, client_required], name='dispatch')
class OffreTransCreateView(CreateView):
    model = OffreCommandeLivraison
    fields = ('designation', 'offre','quantité', 'refproduit', 'categorie', 'transporteur','depart','arrive','datedepart')
    template_name = 'flexible/ajoutOffreTrans.html'
    def get_form(self, *args, **kwargs):
        
        form = super(OffreTransCreateView, self).get_form(*args, **kwargs)

       
        form.fields['offre'].queryset = OffreLivraison.objects.filter(client_id=self.request.user.client)
        return form

    def form_valid(self, form):
        form.instance.client = self.request.user.client
        offre = form.save(commit=False)
        offre.save()
        
        return redirect('multiC')

@method_decorator([login_required, client_required], name='dispatch')
class ReponseView(ListView):
    model = AcceptationLivraison
    context_object_name = 'myreponses'
    template_name = 'flexible/reponsesClient.html'

    
    def get_queryset(self):
        
        queryset = AcceptationLivraison.objects.filter(client_id=self.request.user.client)
        return queryset
    

@method_decorator([login_required, client_required], name='dispatch')
class AllEntrepotsListView(ListView):
    model = Entrepot

    context_object_name = 'depots'
    template_name = 'flexible/allEntrepots.html'
   
    def get_queryset(self):
        queryset = Entrepot.objects.all()
        return queryset

@method_decorator([login_required, client_required], name='dispatch')
class AppreciationsCreateView(CreateView):
    model = Appreciation
    fields =  '__all__' 

    template_name = 'flexible/addAppreciation.html'

    def form_valid(self, form):
        
        Appreciation = form.save(commit=False)
        Appreciation.save()
        
        return redirect('reponsesClient')



@method_decorator([login_required,client_required], name='dispatch')
class BaseView(ListView):
    data = dict()
    template_name = 'flexible/multiView.html'
    def get(self, request):
        self.data['partenaires'] = Partenaire.objects.prefetch_related('places').all()
        return render_to_response(self.template_name, self.data) 

@method_decorator([login_required, partenaire_required], name='dispatch')
class BaseViewP(ListView):
    data = dict()
    template_name = 'flexible/multiView.html'
    def get(self, request):
        self.data['partenaires'] = Partenaire.objects.prefetch_related('places').all()
        return render_to_response(self.template_name, self.data) 


class AppreciationsListView(ListView):
    model = Appreciation

    context_object_name = 'appreciations'
    template_name = 'flexible/appreciations.html'
   
    def get_queryset(self):
        queryset = Appreciation.objects.all()
        return queryset


#partie de la suiviStock et SuiviTransporteur

# The `chart` function is defined to generate Column 2D chart from database.
def chart(request):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Les entrepots classements",
            "subCaption": "AbdouwerChart",
            "xAxisName": "Entrepot",
            "yAxisName": "Capacité",
            "numberPrefix": "Palettes ",
            "theme": "zune"
        }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.
    
    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    for key in Place.objects.filter(state=False):
      data = {}
      data['label'] = key.entrepot.designation
      data['value'] = key.nb_palettes
     
      dataSource['data'].append(data)

    # Create an object for the Column 2D chart using the FusionCharts class constructor
    column3D = FusionCharts("column3D", "ex1" , "600", "350", "chart-1", "json", dataSource)
    return render(request, 'flexible/multiView.html', {'output': column3D.render()})

