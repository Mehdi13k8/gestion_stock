# Create your views here.

from django.shortcuts import render, render_to_response, redirect
from .models import *
from django.views.generic import ListView
from django import forms
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from collections import namedtuple
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

#https://realpython.com/django-and-ajax-form-submissions/ faut aller apprendre la connection
#https://code.djangoproject.com/wiki/AjaxDojoLogin

class index(ListView):
    template_name = "index.html"

    def get(self, request):
        context = {
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

class index_login(ListView):
    template_name = "login.html"

    def loginajax(request):
        manipulator = AuthenticationForm(request)
        redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
        if request.POST:
            errors = manipulator.get_validation_errors(request.POST)
            if not errors:
                if not redirect_to or '://' in redirect_to or ' ' in redirect_to:
                    redirect_to = '/accounts/profile/'
                request.session[SESSION_KEY] = manipulator.get_user_id()
                request.session.delete_test_cookie()
                return HttpResponse(redirect_to)
            else:
                return HttpResponse("false")

    def get(self, request):
        context = {
            'activate' : 'on'
        }
        return render_to_response(self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#site d'importation

class BonCommandeEntree_index(ListView):
    template_name = "bonCommandeEntree.html"

    def delete(request):
        if request.method == 'POST':
            #objects.get avec un filtre retourne le seul objet a avoir le même idboncommandeentree
            one_task = BonCommandeEntree.objects.get(idBonCommandeEntree=request.POST['id'])
            one_task.delete()
            return HttpResponse("deleted !")

    def get(self, request):
        context = {
            'bone' : BonCommandeEntree.objects.all(),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

class BonCommandeEntreeadd(ListView):
    template_name = "bonCommandeEntreeadd.html"

    def add(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'),
                        request.POST.get('ncommande'), request.POST.get('datecom')]

            bce = BonCommandeEntree.objects.all()
            foundit = 0
            for items in bce:
                if items.idBonCommandeEntree == showlist[0]:
                    foundit = 1
                    return HttpResponse("found")
            if foundit == 0: #je crée un bcs
                boncome = BonCommandeEntree()
                boncome.idBonCommandeEntree = showlist[0]
                boncome.numeroCommande = showlist[1]
                boncome.dateCommande = showlist[2]
                boncome.save()
            return HttpResponse("added ! " + showlist[0] + showlist[1] + showlist[2])
        return HttpResponse("No access there !")

    def get(self, request):
        context = {
            'bone' : BonCommandeEntree.objects.all(),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

class BonCommandeEntreemodify(ListView):
    template_name = "bonCommandeEntreemodify.html"

    def get(self, request):
        context = {
            'bone' : BonCommandeEntree.objects.all(),
            'id' :request.GET.get('id'),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#c'est le bon de sortie pour les commande
class ListeArticles(ListView):
    data = dict()

    template_name = "bonCommandeSortie.html"

    def get(self, request):
        self.data['lesclients'] = Client_pour_import_BonCommandeSortie.objects.prefetch_related('clients').all()
        context = {
            'sortie' :BonCommandeSortie_pour_import_BonCommandeSortie.objects.all().select_related('fk_Client', 'fk_Destinataire', 'fk_Transporteur', 'fk_TypeBonCommandeSortie'),
            'umsortie':UniteManutentionSortie_pour_BonCommandeSortie.objects.all().select_related('fk_BonCommandeSortie', 'fk_TypeUniteManutentionSortie', 'fk_Etiquette'),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#useless
def bonCommandeSortieadd(request):
    context = {
        'sortie' :BonCommandeSortie_pour_import_BonCommandeSortie.objects.all().select_related('fk_Client', 'fk_Destinataire', 'fk_Transporteur', 'fk_TypeBonCommandeSortie'),
        'umsortie':UniteManutentionSortie_pour_BonCommandeSortie.objects.all().select_related('fk_BonCommandeSortie', 'fk_TypeUniteManutentionSortie', 'fk_Etiquette'),
        'sortiebl':BonLivraisonSortie_pour_BonCommandeSortie.objects.all().select_related('fk_BonCommandeSortie'),
    }
    return render(request, 'bonCommandeSortieadd.html', context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class bonLivraisonEntree(ListView):
    template_name = "bonLivraisonEntree.html"

    def get(self, request):
        context = {
            'entree' : BonLivraisonEntree.objects.all(),
            #'entreeligne' : LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#c'est le bon de sortie pour les commande
class bonLivraisonSortie(ListView):
    template_name = "bonLivraisonSortie.html"

    def get(self, request):
        context = {
            'sortie' :BonLivraisonSortie.objects.all().select_related('fk_BonCommandeSortie', 'fk_LettreVoitureSortie'),
            'sortieligne' :LigneBonLivraisonSortie_pour_BonLivraisonSortie.objects.all().select_related('fk_Article', 'fk_BonLivraisonSortie'),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class bonLivraisonSortieadd(ListView):
    template_name = "bonLivraisonSortieadd.html"

    def get(self, request):
        context = {
            'sortie' :BonLivraisonSortie.objects.all().select_related('fk_BonCommandeSortie', 'fk_LettreVoitureSortie'),
            'sortieligne' :LigneBonLivraisonSortie_pour_BonLivraisonSortie.objects.all().select_related('fk_Article', 'fk_BonLivraisonSortie'),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class article(ListView):
    template_name = "article.html"

    def delete(request):
        if request.method == 'POST':
            article = Article.objects.get(idArticle=request.POST['id'])
            article.delete()
            return HttpResponse("Deleted !")
        return HttpResponse("No Authorized Access !")

    def get(self, request):
        context = {
            'art' : Article.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class articleadd(ListView):
    template_name = "articleadd.html"

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('name'), request.POST.get('id'),
                        request.POST.get('codefour'), request.POST.get('desifour'),
                        request.POST.get('codecli'), request.POST.get('desicli'),

                        request.POST.get('delaicli'), request.POST.get('durestock'),
                        request.POST.get('artitype'), request.POST.get('fournitype'),
                        request.POST.get('qtecstd'), request.POST.get('pcstd'),
                        request.POST.get('source'), request.POST.get('idsource')]
            article = Article()
            article.nom =  showlist[0]
            article.idArticle = showlist[1]
            article.codeFournisseur = showlist[2]
            article.designationFournisseur = showlist[3]
            article.codeClient = showlist[4]
            article.designationClient = showlist[5]
            article.delaiPeremption = showlist[6]
            article.dureeStockage = showlist[7]

            typearticle = typeArticle_pour_Article.objects.all()
            for items in typearticle:
                if items.nom == showlist[8]:
                    article.fk_TypeArticle = items

            fournisseur = Fournisseur.objects.all()
            for items in fournisseur:
                if items.nom == showlist[9]:
                    article.fk_Fournisseur = items
            article.quantiteColisStandard = showlist[10]
            article.poidsColisStandard = showlist[11]
            article.source = showlist[12]
            article.identifiantSource = showlist[13]
            article.save()
            return HttpResponse("New article created !")
        return HttpResponse("Unauthorized page !")

    def get(self, request):
        context = {
            'art' : Article.objects.all(),
            'typeart' : typeArticle_pour_Article.objects.all(),
            'four' : Fournisseur.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import sys

class articlemodify(ListView):
    template_name = "articlemodify.html"

    def modif(request):
        if request.method == 'POST':
            showlist = [request.POST.get('name'), request.POST.get('id'),
                        request.POST.get('codefour'), request.POST.get('desifour'),
                        request.POST.get('codecli'), request.POST.get('desicli'),

                        request.POST.get('delaicli'), request.POST.get('durestock'),
                        request.POST.get('artitype'), request.POST.get('fournitype'),
                        request.POST.get('qtecstd'), request.POST.get('pcstd'),
                        request.POST.get('source'), request.POST.get('idsource')]
            article = Article.objects.get(idArticle=showlist[1])
            article.nom =  showlist[0]
            article.idArticle = showlist[1]
            article.codeFournisseur = showlist[2]
            article.designationFournisseur = showlist[3]
            article.codeClient = showlist[4]
            article.designationClient = showlist[5]
            article.delaiPeremption = showlist[6]
            article.dureeStockage = showlist[7]

            typearticle = typeArticle_pour_Article.objects.all()
            for items in typearticle:
                if items.nom == showlist[8]:
                    article.fk_TypeArticle = items

            fournisseur = Fournisseur.objects.all()
            for items in fournisseur:
                if items.nom == showlist[9]:
                    article.fk_Fournisseur = items
            article.quantiteColisStandard = showlist[10]
            article.poidsColisStandard = showlist[11]
            article.source = showlist[12]
            article.identifiantSource = showlist[13]
            article.save()
            return HttpResponse(" article modified !")
        return HttpResponse("Unauthorized page !")

    def get(self, request):
        context = {
            'art' : Article.objects.all(),
            'typeart' : typeArticle_pour_Article.objects.all(),
            'desart' : Destinataire_pour_Article.objects.all(),
            'histoart ' : Article_historique_pour_Article.objects.all(),
            'four' : Fournisseur.objects.all(),
            'id' :request.GET.get('id'),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

    def left(request):
        if request.method == 'POST':
            before = request.POST['id']
            article = Article.objects.get(idArticle=request.POST['id'])

            for i in range(int(before)-1, 0, -1):
                try:
                    go = Article.objects.get(idArticle=str(i))
                    return HttpResponse(i)
                except Article.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def right(request):
        if request.method == 'POST':
            my_total = Article.objects.count()
            after = request.POST['id']
            article = Article.objects.get(idArticle=request.POST['id'])

            art = Article.objects.all()

            id = 0
            for myart in art:
                if id < int(myart.idArticle):
                    id = int(myart.idArticle)
            print("id = " + str(id) + '\n')

            for i in range(int(after)+1, id+1, 1):
                try:
                    go = Article.objects.get(idArticle=str(i))
                    return HttpResponse(i)
                except Article.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class fournisseur(ListView):
    template_name = "fournisseur.html"

    def get(self, request):
        context = {
            'four' :Fournisseur.objects.all(),
            'typef':TypeFournisseur_pour_Fournisseur.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

def create_four(request):
    typefournisseur = TypeFournisseur_pour_Fournisseur.objects.all()

    if request.method == 'POST':
        fournisseur = Fournisseur()
        fournisseur.idFournisseur = request.POST['id']
        fournisseur.nom =  request.POST['name']
        for items in typefournisseur:
            if items.nom == request.POST.get('fourtype'):
                fournisseur.fk_TypeFournisseur = items
        fournisseur.save()
        return HttpResponse("New fournisseur " + request.POST['name'] + "created !")

def delete_four(request):
    if request.method == 'POST':
        fournisseur = Fournisseur.objects.get(idFournisseur=request.POST['id'])
        fournisseur.delete()
    return HttpResponse("New fournisseur " + request.POST.get['name'] + " del !")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class fournisseuradd(ListView):
    template_name = "fournisseuradd.html"

    def get(self, request):
        context = {
            'four' : Fournisseur.objects.all(),
            'typef':TypeFournisseur_pour_Fournisseur.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class fournisseurmodify(ListView):
    template_name = "fournisseurmodify.html"

    def modify(request):
        if request.method == 'POST':
            fourni = Fournisseur.objects.get(idFournisseur=request.POST.get('id'))
            fourni.nom = request.POST.get('name')
            fournitype = TypeFournisseur_pour_Fournisseur.objects.all()
            for items in fournitype:
                if items.nom == request.POST.get('fournitype'):
                    fourni.fk_TypeFournisseur = items
            fourni.save()
            return HttpResponse("you think its good ? fournisseur " + request.POST['name'] + " updated !")

    def left(request):
        if request.method == 'POST':
            before = request.POST['id']
            fournisseur = Fournisseur.objects.get(idFournisseur=request.POST['id'])

            for i in range(int(before)-1, 0, -1):
                try:
                    go = Fournisseur.objects.get(idFournisseur=str(i))
                    return HttpResponse(i)
                except Fournisseur.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def right(request):
        if request.method == 'POST':
            my_total = Fournisseur.objects.count()
            after = request.POST['id']
            fournisseur = Fournisseur.objects.get(idFournisseur=request.POST['id'])

            fou = Fournisseur.objects.all()

            id = 0
            for myfou in fou:
                if id < int(myfou.idFournisseur):
                    id = int(myfou.idFournisseur)
            print("id = " + str(id))

            for i in range(int(after)+1, id+1, 1):
                try:
                    print("id = " + str(id))
                    go = Fournisseur.objects.get(idFournisseur=str(i))
                    return HttpResponse(i)
                except Fournisseur.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def get(self, request):
        context = {
            'four' : Fournisseur.objects.all(),
            'name' : request.GET.get('name'),
            'id' : request.GET.get('id'),
            'typef': TypeFournisseur_pour_Fournisseur.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class transporteur(ListView):
    template_name = "transporteur.html"

    def get(self, request):
        context = {
            'trans' :Transporteur.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class transporteuradd(ListView):
    template_name = "transporteuradd.html"

    def get(self, request):
        context = {
            'trans' :Transporteur.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

def create_trans(request):
    if request.method == 'POST':
        transporteur = Transporteur()
        transporteur.idTransporteur = request.POST['id']
        transporteur.nom =  request.POST['name']
        transporteur.save()
    return HttpResponse("New Transporter " + request.POST['name'] + "created !")

def delete_trans(request):
    if request.method == 'POST':
        one_task = Transporteur.objects.get(idTransporteur=request.POST['id'])
        one_task.delete()
        return HttpResponse("Transporteur " + request.POST['name'] + " deleted !")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class transporteurmodify(ListView):
    template_name = "transporteurmodify.html"

    def modify(request):
        if request.method == 'POST':
            transp = Transporteur.objects.get(idTransporteur=request.POST.get('id'))
            transp.nom = request.POST.get('name')
            transp.save()
            return HttpResponse("you think its good ? Transporteur " + request.POST['name'] + " updated !")

    def get(self, request):
        context = {
            'trans' :Transporteur.objects.all(),
            'name' :request.GET.get('name'),
            'id' :request.GET.get('id'),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class destinataire(ListView):
    template_name = "destinataire.html"

    def delete(request):

        dest = Destinataire.objects.all()
        if request.method == 'POST':
            for items in dest:
                if items.idDestinataire == request.POST.get('id'):
                    data = Destinataire.objects.get(idDestinataire=request.POST['id'])
                    data.delete()
                    return HttpResponse("post success for delete on " + request.POST.get('id'))
            return HttpResponse("post Failure on " + request.POST.get('id'))

    def get(self, request):
        context = {
            'des' :Destinataire.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class destinatairemodify(ListView):
    template_name = "destinatairemodify.html"

    def modify(request):
        if request.method == 'POST':
            destinataire = Destinataire.objects.get(idDestinataire=request.POST.get('id'))
            showlist = [request.POST.get('name'), request.POST.get('identifiantBL'),
                        request.POST.get('telephone'), request.POST.get('email'),
                        request.POST.get('codeum'), request.POST.get('contact'),
                        request.POST.get('delaip'), request.POST.get('adressel_1'),
                        request.POST.get('adressel_2'), request.POST.get('adressel_3'),
                        request.POST.get('adressel_4'), request.POST.get('adressel_5'),
                        request.POST.get('adressel_6'), request.POST.get('adressel_7'),
                        request.POST.get('departement'), request.POST.get('adressecom'),
                        request.POST.get('typedest'), request.POST.get('source'),
                        request.POST.get('sourceid'), request.POST.get('nom'),
                        request.POST.get('num'), request.POST.get('rue'),
                        request.POST.get('comp1'), request.POST.get('comp2'),
                        request.POST.get('codepost'), request.POST.get('ville')]

            destinataire.nom = showlist[0]
            destinataire.identifiantBonLivraison = showlist[1]
            destinataire.telephone = showlist[2]
            destinataire.email = showlist[3]
            destinataire.codeUM = showlist[4]
            destinataire.commentaire = showlist[5]
            destinataire.delaiPeremption = showlist[6]

            destinataire.adresseLivraison_nom = showlist[7]
            destinataire.adresseLivraison_numero = showlist[8]
            destinataire.adresseLivraison_rue = showlist[9]
            destinataire.adresseLivraison_complement_1 = showlist[10]
            destinataire.adresseLivraison_complement_2 = showlist[11]
            destinataire.adresseLivraison_codePostal = showlist[12]
            destinataire.adresseLivraison_localite = showlist[13]
            destinataire.save()
            return HttpResponse("you think its good ? Destinataire " + destinataire.nom + " updated !\n and there is "
                                + showlist[0] + '\n' + showlist[1] + '\n' + showlist[2] + '\n'
                                + showlist[3] + '\n' + showlist[4] + '\n' + showlist[5] + '\n'
                                + showlist[6] + '\n' + showlist[7] + '\n' + showlist[8] + '\n'
                                + showlist[9] + '\n' + showlist[10] + '\n' + showlist[11] + '\n'
                                + showlist[12] + '\n' + showlist[13] + '\n' + showlist[14] + '\n'
                                + showlist[15] + '\n' + showlist[16] + '\n' + showlist[17] + '\n'
                                + showlist[18] + '\n' + showlist[19] + '\n' + showlist[20] + '\n'
                                + showlist[21] + '\n' + showlist[22] + '\n' + showlist[23] + '\n'
                                + showlist[24] + '\n' + showlist[25])

    def left(request):
        if request.method == 'POST':
            before = request.POST['id']
            destinataire = Destinataire.objects.get(idDestinataire=request.POST['id'])

            for i in range(int(before)-1, 0, -1):
                try:
                    go = Destinataire.objects.get(idDestinataire=str(i))
                    return HttpResponse(i)
                except Destinataire.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def right(request):
        if request.method == 'POST':
            my_total = Destinataire.objects.count()
            after = request.POST['id']
            destinataire = Destinataire.objects.get(idDestinataire=request.POST['id'])

            des = Destinataire.objects.all()

            id = 0
            for mydes in des:
                if id < int(mydes.idDestinataire):
                    id = int(mydes.idDestinataire)
            print("id = " + str(id))

            for i in range(int(after)+1, id+1, 1):
                try:
                    print("id = " + str(id))
                    go = Destinataire.objects.get(idDestinataire=str(i))
                    return HttpResponse(i)
                except Destinataire.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def get(self, request):
        context = {
            'des' :Destinataire.objects.all(),
            'name' :request.GET.get('name'),
            'id' :request.GET.get('id'),
            'umsortie' :UniteManutentionSortie_pour_Destinataire.objects.all().select_related('fk_BonCommandeSortie'),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class destinataireadd(ListView):
    template_name = "destinataireadd.html"

    def create(request):
        if request.method == 'POST':
            destinataire = Destinataire()
            showlist = [request.POST.get('name'), request.POST.get('identifiantBL'),
                        request.POST.get('telephone'), request.POST.get('email'),
                        request.POST.get('codeum'), request.POST.get('contact'),
                        request.POST.get('delaip'), request.POST.get('adressel_1'),
                        request.POST.get('adressel_2'), request.POST.get('adressel_3'),
                        request.POST.get('adressel_4'), request.POST.get('adressel_5'),
                        request.POST.get('adressel_6'), request.POST.get('adressel_7'),
                        request.POST.get('departement'), request.POST.get('adressecom'),
                        request.POST.get('typedest'), request.POST.get('source'),
                        request.POST.get('sourceid'), request.POST.get('nom'),
                        request.POST.get('num'), request.POST.get('rue'),
                        request.POST.get('comp1'), request.POST.get('comp2'),
                        request.POST.get('codepost'), request.POST.get('ville'),
                        request.POST.get('id')]

            destinataire.nom = showlist[0]
            destinataire.identifiantBonLivraison = showlist[1]
            destinataire.telephone = showlist[2]
            destinataire.email = showlist[3]
            destinataire.codeUM = showlist[4]
            destinataire.commentaire = showlist[5]
            destinataire.delaiPeremption = showlist[6]

            destinataire.adresseLivraison_nom = showlist[7]
            destinataire.adresseLivraison_numero = showlist[8]
            destinataire.adresseLivraison_rue = showlist[9]
            destinataire.adresseLivraison_complement_1 = showlist[10]
            destinataire.adresseLivraison_complement_2 = showlist[11]
            destinataire.adresseLivraison_codePostal = showlist[12]
            destinataire.adresseLivraison_localite = showlist[13]

            destinataire.idDestinataire = showlist[26]

            pays = Pays_pour_Destinataire.objects.all()
            for items in pays:
                if items.nom == request.POST.get('pays'):
                    destinataire.fk_Pays = items

            typedest = TypeDestinataire_pour_Destinataire.objects.all()
            for items in typedest:
                if items.nom == request.POST.get('typedest'):
                    destinataire.fk_TypeDestinataire = items
                    destinataire.save()
                    return HttpResponse("It has been posted by lapost")
            destinataire.save()
            return HttpResponse("Error " + request.POST.get('typedest') + " "+ items.nom)

    def get(self, request):
        context = {
            'destype' :TypeDestinataire_pour_Destinataire.objects.all(),
            'des' :Destinataire.objects.all(),
            'pays':Pays_pour_Destinataire.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class colis(ListView):
    template_name = "colis.html"

    def delete(request):
        if request.method == 'POST':
            col = colis.objects.all()
            for items in col:
                if items.idColis == request.POST.get('id'):
                    data = Colis.objects.get(idColis=request.POST['id'])
                    data.delete()
                    return HttpResponse("road to delete.")
            return HttpResponse("Error on delete.")
        return HttpResponse("Leave this place!")

    def get(self, request):
        context = {
            'col' : Colis.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class client(ListView):
    template_name = "client.html"

    def delete(request):
        if request.method == 'POST':
            cli = Client.objects.all()
            for items in cli:
                if items.idClient == request.POST.get('id'):
                    data = Client.objects.get(idClient=request.POST['id'])
                    data.delete()
                    return HttpResponse("road to delete.")
            return HttpResponse("Error on delete.")
        return HttpResponse("Leave this place!")


    def get(self, request):
        context = {
            'cli' : Client.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

class clientmodify(ListView):
    template_name = "clientmodify.html"

    #Ajout ou supression de contact si non ou existants si présent dans la zone contact
    def modify_cli_contact(request):
        if request.method == 'POST':
            showlist = [request.POST.get('role'), request.POST.get('name'),
                        request.POST.get('prenom'), request.POST.get('tel'),
                        request.POST.get('mail'), request.POST.get('id'),
                        request.POST.get('idcontact'), request.POST.get('totalcontact')]
            #Je cherche dans la table si les contacts recus éxistent
            modify = Contact_pour_Client.objects.all()
            role = RoleContact_pour_Client.objects.all()
            client = Client.objects.get(idClient=showlist[5])

            repetition = 0
            idx = 0
            idcontact = 1
            if not modify:
                print("empty")
                mycontact = Contact_pour_Client()
                mycontact.fk_RoleContact = RoleContact_pour_Client.objects.get(nom=showlist[0])
                mycontact.fk_Client = Client.objects.get(idClient=showlist[5])
                mycontact.nom = showlist[1]
                mycontact.prenom = showlist[2]
                mycontact.telephone = showlist[3]
                mycontact.email = showlist[4]
                mycontact.idContact = idcontact
                mycontact.save()
                return HttpResponse("empty New contact " + showlist[5])
            else:
                for itemsm in modify:
                    role = ""
                    nom = ""
                    prenom = ""
                    tel = ""
                    mail = ""
                    mycli = ""
                    idcontact += 1
                    if (itemsm.fk_RoleContact.nom  == showlist[0]):
                        role = 1
                    if (itemsm.nom == showlist[1]):
                        nom = 1
                    if (itemsm.prenom == showlist[2]):
                        prenom = 1
                    if (itemsm.telephone == showlist[3]):
                        tel = 1
                    if (itemsm.email == showlist[4]):
                        mail = 1
                    if (itemsm.fk_Client.idClient == showlist[5]):
                        mycli = 1
                    if (role == 1 and nom == 1 and prenom == 1 and
                            tel == 1 and mail == 1 and mycli == 1):
                        repetition += 1
                        return HttpResponse("One of the contact aldready exist")
                        break
                    idx+=1
                    if not showlist[6]:
                        mycontact = Contact_pour_Client()
                    else:
                        mycontact = Contact_pour_Client.objects.get(idContact=showlist[6])
                    mycontact.fk_RoleContact = RoleContact_pour_Client.objects.get(nom=showlist[0])
                    mycontact.fk_Client = Client.objects.get(idClient=showlist[5])
                    mycontact.nom = showlist[1]
                    mycontact.prenom = showlist[2]
                    mycontact.telephone = showlist[3]
                    mycontact.email = showlist[4]
                    if not showlist[6]:
                        mycontact.idContact = showlist[7]
                    mycontact.save()
                    return HttpResponse("New contact " + ' ' + showlist[0] + ' ' + showlist[1] + ' ' + showlist[2] + ' ' + showlist[3] + ' ' + showlist[4] + ' ' + showlist[6])
                #elif repetition > 0 and not showlist[6]:
                '''mycontact = Contact_pour_Client.objects.get(idContact=showlist[6])
                mycontact.fk_RoleContact = RoleContact_pour_Client.objects.get(nom=showlist[0])
                mycontact.fk_Client = Client.objects.get(idClient=showlist[5])
                mycontact.nom = showlist[1]
                mycontact.prenom = showlist[2]
                mycontact.telephone = showlist[3]
                mycontact.email = showlist[4]
                mycontact.idContact = idcontact
                mycontact.save()'''
                return HttpResponse("One of the contact aldready exist modfying it")
            return HttpResponse("road to post con")
        return HttpResponse("403: what are you doing there?")

    def delete_cli_contact(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            print("id = "+ request.POST.get('id'))
            mycontact = Contact_pour_Client.objects.get(idContact=request.POST['id'])
            mycontact.delete()

            return HttpResponse("road to post del con")
        return HttpResponse("403: what are you doing there?")

    def modify(request):
        if request.method == 'POST':
            showlist = [request.POST.get('nom'), request.POST.get('id'),
                        request.POST.get('telephone'), request.POST.get('email'),
                        request.POST.get('tva'), request.POST.get('siret'),
                        request.POST.get('adresse'), request.POST.get('zone'),
                        request.POST.get('typedest'), request.POST.get('typefour'),
                        request.POST.get('typeart'), request.POST.get('source'),
                        request.POST.get('idsource'), request.POST.get('boncs'),
                        request.POST.get('bonle'), request.POST.get('odt'),
                        request.POST.get('cont'), request.POST.get('commentaire')]

            client = Client.objects.get(idClient=showlist[1])

            zne = TypeZoneDepot_pour_Client.objects.all()
            znedebug = False
            for zone in zne:
                if request.POST.get('zone') == zone.nom:
                    znedebug = True
                    client.fk_TypeZone = zone
                tde = TypeDestinataire_pour_Client.objects.all()
                tdedebug = False
            for typed in tde:
                if request.POST.get('typedest') == typed.nom:
                    tdedebug = True
                    client.fk_TypeDestinataire = typed
                tfo = TypeFournisseur_pour_Client.objects.all()
                tfodebug = False
            for typefo in tfo:
                if request.POST.get('typefour') == typefo.nom:
                    tfodebug = True
                client.fk_TypeFournisseur = typefo
                tar = TypeArticle_pour_Client.objects.all()
                tardebug = False
            for typea in tar:
                if request.POST.get('typeart') == typea.nom:
                    tardebug = True
                client.fk_TypeArticle = typea

            client.nom = showlist[0]
            client.idClient = showlist[1]
            client.telephone = showlist[2]
            client.email = showlist[3]
            client.tva = showlist[4]
            client.siret = showlist[5]
            client.adresse = showlist[6]
            client.source = showlist[11]
            client.identifiantSource = showlist[12]
            client.commentaire = showlist[17]
            client.save()
            return HttpResponse("road to post mod")
        return HttpResponse("403: what are you doing there?")

    def left(request):
        if request.method == 'POST':
            before = request.POST['id']
            client = Client.objects.get(idClient=request.POST['id'])

            for i in range(int(before)-1, 0, -1):
                try:
                    go = Client.objects.get(idClient=str(i))
                    return HttpResponse(i)
                except Client.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def right(request):
        if request.method == 'POST':
            my_total = Client.objects.count()
            after = request.POST['id']
            client = Client.objects.get(idClient=request.POST['id'])

            cli = Client.objects.all()

            id = 0
            for mycli in cli:
                if id < int(mycli.idClient):
                    id = int(mycli.idClient)
            print("id = " + str(id))

            for i in range(int(after)+1, id+1, 1):
                try:
                    print("id = " + str(id))
                    go = Client.objects.get(idClient=str(i))
                    return HttpResponse(i)
                except Client.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def get(self, request):
        context = {
            'cli' : Client.objects.all(),
            'con' : Contact_pour_Client.objects.all(),
            'rlc' : RoleContact_pour_Client.objects.all(),
            'id' :request.GET.get('id'),
            'typez' : TypeZoneDepot_pour_Client.objects.all(),
            'typed' : TypeDestinataire_pour_Client.objects.all(),
            'typef' : TypeFournisseur_pour_Client.objects.all(),
            'typea' : TypeArticle_pour_Client.objects.all(),
            'bcs' : BonCommandeSortie.objects.all(),
            'bce' : BonCommandeEntree.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

class clientadd(ListView):
    template_name = "clientadd.html"

    def create(request):
        if request.method == 'POST':
            array = {}
            showlist = [request.POST.get('nom'), request.POST.get('id'),
                        request.POST.get('telephone'), request.POST.get('email'),
                        request.POST.get('tva'), request.POST.get('siret'),
                        request.POST.get('adresse'), request.POST.get('zone'),
                        request.POST.get('typedest'), request.POST.get('typefour'),
                        request.POST.get('typeart'), request.POST.get('source'),
                        request.POST.get('idsource'), request.POST.get('boncs'),
                        request.POST.get('bonle'), request.POST.get('odt'),
                        request.POST.get('cont'), request.POST.get('commentaire')]

            client = Client()
            cli = Client.objects.all()
            for items in cli:
                if items.idClient == request.POST.get('id'):
                    return HttpResponse("Client aldready registered")

            zne = TypeZoneDepot_pour_Client.objects.all()
            znedebug = False
            for zone in zne:
                if request.POST.get('zone') == zone.nom:
                    znedebug = True
                    client.fk_TypeZone = zone
                tde = TypeDestinataire_pour_Client.objects.all()
                tdedebug = False
            for typed in tde:
                if request.POST.get('typedest') == typed.nom:
                    tdedebug = True
                    client.fk_TypeDestinataire = typed
                tfo = TypeFournisseur_pour_Client.objects.all()
                tfodebug = False
            for typefo in tfo:
                if request.POST.get('typefour') == typefo.nom:
                    tfodebug = True
                client.fk_TypeFournisseur = typefo
                tar = TypeArticle_pour_Client.objects.all()
                tardebug = False
            for typea in tar:
                if request.POST.get('typeart') == typea.nom:
                    tardebug = True
                client.fk_TypeArticle = typea
            if tfodebug is False:
                return HttpResponse(" Error you choosed a broken fk")
            if znedebug is False:
                return HttpResponse(" Error you choosed a broken fk")
            if tdedebug is False:
                return HttpResponse(" Error you choosed a broken fk")
            if tardebug is False:
                return HttpResponse(" Error you choosed a broken fk")
            else:
                client.nom = showlist[0]
                client.idClient = showlist[1]
                client.telephone = showlist[2]
                client.email = showlist[3]
                client.tva = showlist[4]
                client.siret = showlist[5]
                client.adresse = showlist[6]
                client.source = showlist[11]
                client.identifiantSource = showlist[12]
                client.commentaire = showlist[17]
                client.save()
                return HttpResponse("GG Client created ")
            '''array["role"] = request.POST.get('role')
            array["name"] = request.POST.get('name')
            array["prenom"] = request.POST.get('prenom')
            array["tel"] = request.POST.get('tel')
            array["mail"] = request.POST.get('mail')

            client = Client()
            cli = Client.objects.all()
            existcli = False
            existcont = False
            for items in cli:
                if items.idClient == request.POST.get('id'):
                    existcli = True
                    print("existing")
                    client = Client.objects.get(idClient=request.POST.get('id'))

            if existcli is True:
                zne = TypeZoneDepot_pour_Client.objects.all()
                znedebug = False
                for zone in zne:
                    if request.POST.get('zone') == zone.nom:
                        znedebug = True
                        client.fk_TypeZone = zone                #fin
                # fk_typedest donc parcourir sa table
                tde = TypeDestinataire_pour_Client.objects.all()
                tdedebug = False
                for typed in tde:
                    if request.POST.get('typedest') == typed.nom:
                        tdedebug = True
                        client.fk_TypeDestinataire = typed                #fin
                # fk_typefour donc parcourir sa table
                tfo = TypeFournisseur_pour_Client.objects.all()
                tfodebug = False
                for typefo in tfo:
                    if request.POST.get('typefour') == typefo.nom:
                        tfodebug = True
                        client.fk_TypeFournisseur = typefo                #fin
                #fk_typear donc parcourir sa table
                tar = TypeArticle_pour_Client.objects.all()
                tardebug = False
                for typea in tar:
                    if request.POST.get('typeart') == typea.nom:
                        #print("targood" +'\n')
                        tardebug = True
                        client.fk_TypeArticle = typea
                if tfodebug is False:
                    print("tfodebug is false")
                    return HttpResponse(" Error you choosed a broken fk")
                if znedebug is False:
                    print("znedebug is false")
                    return HttpResponse(" Error you choosed a broken fk")
                if tdedebug is False:
                    print("tdedebug is false")
                    return HttpResponse(" Error you choosed a broken fk")
                if tardebug is False:
                    print("tardebug is false")
                    return HttpResponse(" Error you choosed a broken fk")
                else:
                    concli = Contact_pour_Client.objects.all()
                    conid = 1
                    for con in concli:
                        conid += 1
                    #print(conid)
                    contact = Contact_pour_Client()
                    contact.fk_Client = client #request.POST.get('id')
                    role = RoleContact_pour_Client.objects.all() #getrolecontact
                    for rolec in role:
                        if request.POST.get('role') == rolec.nom:
                            contact.fk_RoleContact = rolec
                    contact.name = request.POST.get('name')
                    contact.prenom = request.POST.get('prenom')
                    contact.tel = request.POST.get('tel')
                    contact.mail = request.POST.get('mail')
                    if contact.name is None:
                        return HttpResponse("Contact error for existing cli")
                    if contact.prenom is None:
                        return HttpResponse("Contact error for existing cli")
                    if contact.tel is None:
                        return HttpResponse("Contact error for existing cli")
                    if contact.name is None:
                        return HttpResponse("Contact error for existing cli")
                    contact.save()
                    #print("gg cli exist")
                return HttpResponse("Client aldready existing")

            else: #La on a donc la partie création d'un utilisateur avec check de sécu
                print("Not existing")
                # fk_Zonetype donc parcourir sa table
                zne = TypeZoneDepot_pour_Client.objects.all()
                znedebug = False
                for zone in zne:
                    if request.POST.get('zone') == zone.nom:
                        znedebug = True
                        client.fk_TypeZone = zone
                #fin
                # fk_typedest donc parcourir sa table
                tde = TypeDestinataire_pour_Client.objects.all()
                tdedebug = False
                for typed in tde:
                    if request.POST.get('typedest') == typed.nom:
                        tdedebug = True
                        client.fk_TypeDestinataire = typed
                #fin
                # fk_typefour donc parcourir sa table
                tfo = TypeFournisseur_pour_Client.objects.all()
                tfodebug = False
                for typefo in tfo:
                    if request.POST.get('typefour') == typefo.nom:
                        tfodebug = True
                        client.fk_TypeFournisseur = typefo
                #fin
                #fk_typear donc parcourir sa table
                tar = TypeArticle_pour_Client.objects.all()
                tardebug = False
                for typea in tar:
                    if request.POST.get('typeart') == typea.nom:
                        #print("targood" +'\n')
                        tardebug = True
                        client.fk_TypeArticle = typea
                #fin
                if tfodebug is False:
                    print("tfodebug is false")
                    return HttpResponse(" Error you choosed a broken fk")
                if znedebug is False:
                    print("znedebug is false")
                    return HttpResponse(" Error you choosed a broken fk")
                if tdedebug is False:
                    print("tdedebug is false")
                    return HttpResponse(" Error you choosed a broken fk")
                if tardebug is False:
                    print("tardebug is false")
                    return HttpResponse(" Error you choosed a broken fk")
                else:
                    client.nom = showlist[0]
                    client.idClient = showlist[1]
                    client.telephone = showlist[2]
                    client.email = showlist[3]
                    client.tva = showlist[4]
                    client.siret = showlist[5]
                    client.adresse = showlist[6]
                    client.source = showlist[11]
                    client.identifiantSource = showlist[12]
                    client.commentaire = showlist[17]
                    client.save()
                    concli = Contact_pour_Client.objects.all()
                    conid = 1
                    for con in concli:
                        conid += 1
                    #print(conid)
                    contact = Contact_pour_Client()
                    contact.fk_Client = client #request.POST.get('id')
                    role = RoleContact_pour_Client.objects.all() #getrolecontact
                    for rolec in role:
                        if request.POST.get('role') == rolec.nom:
                            contact.fk_RoleContact = rolec
                    contact.name = request.POST.get('name')
                    contact.prenom = request.POST.get('prenom')
                    contact.tel = request.POST.get('tel')
                    contact.mail = request.POST.get('mail')
                    contact.idContact = conid
                    save = 0
                    if contact.name is None:
                        save = 1
                        #return HttpResponse("Contact error for existing cli")
                    if contact.prenom is None:
                        save = 1
                    #print(contact.prenom)
                        #return HttpResponse("Contact error for existing cli")
                    if contact.tel is None:
                        save = 1
                        #return HttpResponse("Contact error for existing cli")
                    if contact.name is None:
                        save = 1
                        #return HttpResponse("Contact error for existing cli")
                    if save != 1:
                        contact.save()
                    return HttpResponse("New Client")
                #for items in cli:'''
            return HttpResponse("GG Client created ")
        return HttpResponse(" You shall not pass! ")

    def fill_contact(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('role'),
                        request.POST.get('name'), request.POST.get('prenom'),
                        request.POST.get('tel'), request.POST.get('mail')]

            concli = Contact_pour_Client.objects.all()
            conid = 1
            for con in concli:
                conid += 1
            contact = Contact_pour_Client()
            contact.fk_Client = Client.objects.get(idClient=showlist[0])
            print("show list 0 " + showlist[0])
            role = RoleContact_pour_Client.objects.all() #getrolecontact
            for rolec in role:
                if showlist[1] == rolec.nom:
                    contact.fk_RoleContact = rolec
            contact.nom = request.POST.get('name')
            contact.prenom = request.POST.get('prenom')
            contact.telephone = request.POST.get('tel')
            contact.email = request.POST.get('mail')
            contact.idContact = conid
            save = 0
            if contact.nom is None:
                save = 1
            if contact.prenom is None:
                save = 1
            if contact.telephone is None:
                save = 1
            if contact.email is None:
                save = 1
            if save != 1:
                contact.save()
            '''| save != 4
             for con in concli:
                if contact.nom == con.nom:
                    save += 1
                if contact.prenom == con.prenom:
                    save += 1
                if contact.telephone == con.telephone:
                    save += 1
                if contact.email == con.email:
                    save += 1
            if save == 4:
                return HttpResponse("contact aldready existing!")
            '''
            return HttpResponse("Success! ")
        return HttpResponse("Who are you?")

    def get(self, request):
        context = {
            'cli' : Client.objects.all(),
            'typez' : TypeZoneDepot_pour_Client.objects.all(),
            'typed' : TypeDestinataire_pour_Client.objects.all(),
            'typef' : TypeFournisseur_pour_Client.objects.all(),
            'typea' : TypeArticle_pour_Client.objects.all(),
            'bcs' : BonCommandeSortie.objects.all(),
            'bce' : BonCommandeEntree.objects.all(),
            'rlc' : RoleContact_pour_Client.objects.all(),
            'con' : Contact_pour_Client.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#unitemanutention

class ume(ListView):
    template_name = "unitemanutentionentree.html"

    def delete(request):
        if request.method == 'POST':
            cli = Client.objects.all()
            for items in cli:
                if items.idClient == request.POST.get('id'):
                    data = Client.objects.get(idClient=request.POST['id'])
                    data.delete()
                    return HttpResponse("road to delete.")
            return HttpResponse("Error on delete.")
        return HttpResponse("Leave this place!")

    def get(self, request):
        context = {
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

class umeadd(ListView):
    template_name = "unitemanutentionentreeadd.html"

    def create(request):
        if request.method == 'POST':
            cli = Client.objects.all()
            for items in cli:
                if items.idClient == request.POST.get('id'):
                    data = Client.objects.get(idClient=request.POST['id'])
                    data.delete()
                    return HttpResponse("road to delete.")
            return HttpResponse("Error on delete.")

    def get(self, request):
        context = {
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

class umemodify(ListView):

    def modify(self, request):
        context = {
        }
        return render(request, self.template_name, context)


    def get(self, request):
        context = {
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
