from django import forms
from .models import Schedule,chose,User,Client,Produit,Transporteur,Partenaire,Entrepot,Appreciation,OffreLivraison,AcceptationLivraison,Appreciation
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.views.generic import TemplateView


class ConnexionForm(forms.Form):

    username = forms.CharField(label="Nom d'utilisateur", max_length=30)

    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = "__all__"

class ClientTestSignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        
        model = User
        fields = ('username','nom','adresse')
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.password = 'test'

        user.save()
        client = Client.objects.create(user=user)
        
        return user

class ClientSignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        
        model = User
        fields = ('username','nom','adresse')
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True

        user.save()
        client = Client.objects.create(user=user)
        
        return user


class PartenaireSignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        
        model = User
        fields = ('username','nom','adresse')
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_partenaire = True
        user.save()
        partenaire = Partenaire.objects.create(user=user)
        
        return user

class TransporteurSignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        
        model = User
        fields = ('username','nom','adresse')
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_transporteur = True
        user.save()
        transporteur = Transporteur.objects.create(user=user)
        
        return user



class ChoseForm(forms.ModelForm):

    class Meta:
        model = chose
        fields = ('title', 'body')