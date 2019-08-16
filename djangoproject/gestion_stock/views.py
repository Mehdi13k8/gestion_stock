# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from .models import *
#from .forms import UploadFileForm
#from .models import ModelWithFileField
from django import forms
#from gestion_stock.forms import ImgaccueilForm
#from gestion_stock.forms import MyCommentForm
#from .forms import UploadFileForm
from .forms import PostForm
from django.urls import reverse, reverse_lazy # new
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import csv, io
import time
#https://realpython.com/django-and-ajax-form-submissions/ faut aller apprendre la connection | plus besoin, connection acquise
#https://code.djangoproject.com/wiki/AjaxDojoLogin

class index(ListView):              #Page d'acceuil vide pour l'instant
    template_name = "index.html" #template html visé situé dans /templates

    def get(self, request):
        img = menuimages.objects.filter(id=1)  #je crée la ligne des "images" pour le menu si on recrée une bdd
        try:
            img = menuimages.objects.get(pk=1)
        except menuimages.DoesNotExist:
            img = None
        if img == None:
            img = menuimages()
            img.id = 1
            img.title = "Menus"
            img.save()
            print("created an image entry for menu")
        context = {
            'activate' : 'on', #cette donnée me permettra de savoir dans quel view je suis pour mettre en surbrillance la page choisie
            'settings' : menuimages.objects.all(),
        }
        return render(request, self.template_name, context) #je retourne le template via self car il se trouve dans la classe la request que django sache ce que je fais et context pour les variables

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #J'étais partie sur cette façon de me connecter, mais je suis retournée a la manière standard offerte par django via un "form standard"
'''class index_login(ListView): 
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
        return render_to_response(self.template_name, context)'''

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
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
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
            'settings' : menuimages.objects.all(),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

class BonCommandeEntreemodify(ListView):
    template_name = "bonCommandeEntreemodify.html"

    def get(self, request):
        context = {
            'bone' : BonCommandeEntree.objects.all(),
            'id' :request.GET.get('id'),
            'settings' : menuimages.objects.all(),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from .forms import UploadFileForm

class bonCommandeSortie(ListView):
    template_name = "bonCommandeSortie.html"

    def delete(request):
        if request.method == 'POST':
            #objects.get avec un filtre retourne le seul objet a avoir le même idboncommandeentree
            one_task = BonCommandeSortie.objects.get(idBonCommandeSortie=request.POST['id'])
            one_task.delete()
            return HttpResponse("deleted !")
        return HttpResponse("No access !")

    def upload_bcsf(request):
        if request.method == 'POST':
            fichier = request.FILES.get('file', False)
            idinput = request.POST.get('idinput')
            bcs = BonCommandeSortie.objects.get(idBonCommandeSortie=idinput)
            bcs.fichier = None
            bcs.fichier = fichier
            bcs.save()
            print("gg fichier sauvegarder !!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(reverse('bonCommandeSortiemodify')+"?id="+bcs.idBonCommandeSortie)
        return HttpResponse("No access authorized !")

    def get(self, request):
        context = {
            'bcs' : BonCommandeSortie.objects.all(),
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'form'     : UploadFileForm(),
            #'order'   : 'Order of CSV should be idBonCommandeSortie, Client, Destinataire, codeDestinataire, Transporteur, numeroCommande, dateCommande, source',
        }
        return render(request, self.template_name, context)

# fonction qui gère l'envoi d'un fichier csv qu'il soit bon de commande sortie ou ligne bon de commande sortie
from datetime import datetime, date

def uploadbc(request):
    data = {
        'bone' : BonCommandeEntree.objects.all(),
        'activate' : 'on',
        'settings' : menuimages.objects.all(),
        'form'     : UploadFileForm(),
    }
    if "GET" == request.method: #si j'ai un get c pas bon car ma "fonction" action dans la forme bon commande sortie m'envoie un POST, donc c'est une "intrusion" non voulu, donc redirection vers boncommandesortie
        return render(request, "bonCommandeSortie.html", data)
    # if not GET, then proceed car c'est bien une requête post que j'ai moi même instancié par un "submite"
    try:
        csv_file = request.FILES["csv_file"] #je récupère le fichier "csv_file" je l'ai nommé comme ça dans le nom de l'input présent dans le form de boncommandesortie
        if (not csv_file.name.endswith('.tab')): # Filemaker sort des formats .tab et non des .csv, les 2 peuvent être réstitué via les ',' mais ce n'est pas le même format, il faut explicitement bloquer les autres types
            messages.error(request,'File is not a Tab type') #j'envoie une erreur au panel admin si ce n'est pas un '.tab'
            print ("File push is not a tab "+csv_file.name.endswith('.tab')+" !!!") #message dans la console pour mon debug
            return HttpResponseRedirect(reverse("bonCommandeSortie")) #donc mauvais fichier = renvoie vers le template de boncommandesortie et non prise en compte du fichier
        #if file is too large, return soit si le fichier dépasse la taille limite d'un seul "read" je crois 64kb je bloque sinon il faut faire plusieurs "read" de chunks, autant limité la taille d'un fichier ça permet aussi d'éviter de trop remplir la bdd en peu de temps
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            print ("Uploaded file is too big")
            return HttpResponseRedirect(reverse("bonCommandeSortie"))
        file_data = csv_file.read().decode('utf-8', errors='ignore') #ici je veux récuperer les "datas" présentes dans le csv, de préférence en utf-8 car majoritairement les tech utilisent utf-8, j'ignore les erreurs pour gagner du temps
        lines = file_data.split("\n")  #je crée plusieurs rows dans mon "array" chaque \n (saut de ligne) équivaut a une "ligne" (rows) donc pour chaque lignes je recrée une "lignes" dans un array
        data_dict = {} #je crée un dictionnaire pour l'utiliser pour un stockage par "clé" qui va s'avéré plus pratique que par index "numérique"
        idx = 0 #pour lire la 1er ligne & voir si la clé est une "ligne" ou un "bon"
        type_csv = 2 #valeurs de check qui me sert a savoir quel type de fichier je recois un fichier pour les bons ou les lignes de bons, elle reste a 2 si le fichier est pas bon
        for line in lines:
            line = line.strip() # j'enlève les lignes vides de la prise en compte si elles sont "vides"
            if line:#seulement si une "ligne" éxiste je la prends en compte pour éviter les erreurs type "out of index" ou "index error"
                fields = line.split(',') #comme presque tout csv sont découper par des ',' je dis a python de me faire une array a chaque ',' (équivalent des colones) ça permet d'éviter l'algo manuel
                if idx == 0:
                    idx+=1 #j'utilise cette var a 0 car elle me permet de "check" la 1er ligne pour vérifier si toutes les colones ont les bons "noms de rubrique" selon type_csv 1 || type csv 2
                    messages.success(request,fields[0]) #message de réussite a la page admin pour lui envoyé le type si bon ou ligne (message de débug pour developpeur)
                    if fields[0] == "﻿idBonCommandeSortie":  #Je compare si c'est un Bon de commande ou si c'est une ligne et avec type csv je mets les clé adéquates
                        messages.success(request,"This is a bon de commande sortie")
                        type_csv = 1 #si c'est un "bondecommande" je le mets a 1
                    if fields[0] == "﻿idLigneBonCommandeSortie":
                        messages.success(request,"This is a Ligne de bon de commande sortie")
                        type_csv = 0 # a 0 cela signifie que c'est une ligne pour bon de commande
                    #mtn je compare si toutes les "têtes" de colones sont bonnes sinon on retourne a la page boncommandesortie & on envoie une erreur  a la page admin
                    if type_csv == 2:
                        messages.error(request,"Unable to upload file Bad Keys at text. give either a good bon commande or ligne bon commande")
                        return HttpResponseRedirect(reverse("bonCommandeSortie"))
                    if len(fields) != 8:
                        messages.error(request,"Unable to upload file Bad Keys at text you need 8 columns.")#les 2 fichiers doivent avoir 8 colones sinon erreur
                        return HttpResponseRedirect(reverse("bonCommandeSortie"))

                    #Vérification des "clé" une par une
                    if type_csv == 1:
                        if not fields[1] == "Client":
                            messages.error(request,"Unable to upload file Bad Keys for lbcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[2] == "Destinataire":
                            messages.error(request,"Unable to upload file Bad Keys for lbcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[3] == "codeDestinataire":
                            messages.error(request,"Unable to upload file Bad Keys for lbcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[4] == "Transporteur":
                            messages.error(request,"Unable to upload file Bad Keys for lbcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[5] == "numeroCommande":
                            messages.error(request,"Unable to upload file Bad Keys for lbcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[6] == "dateCommande":
                            messages.error(request,"Unable to upload file Bad Keys for lbcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[7] == "source":
                            messages.error(request,"Unable to upload file Bad Keys for lbcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                    if type_csv == 0:
                        if not fields[1] == "fk_BonCommandeSortie":
                            messages.error(request,"Unable to upload file Bad Keys for bcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[2] == "Article":
                            messages.error(request,"Unable to upload file Bad Keys .")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[3] == "designation":
                            messages.error(request,"Unable to upload file Bad Keys for bcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[4] == "quantiteProduitCommande":
                            messages.error(request,"Unable to upload file Bad Keys for bcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[5] == "priorite":
                            messages.error(request,"Unable to upload file Bad Keys for bcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[6] == "termine":
                            messages.error(request,"Unable to upload file Bad Keys for bcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        if not fields[7] == "source":
                            messages.error(request,"Unable to upload file Bad Keys for bcs.")
                            return HttpResponseRedirect(reverse("bonCommandeSortie"))

                #puis je dois checker chaque entrée qui utilise un id ou un fk, pour voir si il existe si le "fk" sinon une erreur puis enrigistré
                else:
                    if type_csv == 1:
                        try:
                            fields[6] = datetime.strptime(fields[6], "%d/%m/%Y").strftime("%Y-%m-%d") #le format des dates dans les csv ne sont pas standard donc je la modifie
                            BonCommandeSortie.objects.update_or_create(
                                idBonCommandeSortie=fields[0],
                                fk_Client=Client.objects.get(nom=fields[1]),
                                fk_Destinataire=Destinataire.objects.get(codeUM=fields[3]),
                                fk_Transporteur=Transporteur.objects.get(nom=fields[4]),
                                numeroCommande=fields[5],
                                dateCommande=fields[6],
                                source=fields[7],
                            )
                            #Ici je crée une "UM" sortie pour chaque bon de commande sortie recus & valide
                            #ums = UniteManutentionSortie.objects.get_or_create(fk_BonCommandeSortie=fields[0])
                            try:
                                try:
                                    var = BonCommandeSortie.objects.get(idBonCommandeSortie=fields[0])
                                except BonCommandeSortie.DoesNotExist:
                                    var = None
                                go = UniteManutentionSortie.objects.get(fk_BonCommandeSortie=var)
                            except UniteManutentionSortie.DoesNotExist:
                                go = UniteManutentionSortie()
                                try:
                                    go.idUniteManutentionSortie = str(UniteManutentionSortie.objects.latest('idUniteManutentionSortie'))
                                    go.idUniteManutentionSortie = str(int(go.idUniteManutentionSortie) + int(1))
                                except UniteManutentionSortie.DoesNotExist:
                                    go.idUniteManutentionSortie = str(1)
                                go.fk_BonCommandeSortie = var #les try et except me permettent d'éviter une "erreur" dans
                                go.fk_BonLivraisonSortie = None
                                go.dateOuverture = time.strftime("%Y-%m-%d")
                            go.save()
                            #ums.idUniteManutentionSortie = UniteManutentionSortie.objects.latest('idUniteManutentionSortie')
                            messages.success(request,"Succès -> Donnees du Csv ont ete ajoutees aux  tarifs")
                        except Exception as e:
                            messages.warning(request," Votre fichier n'est pas conforme à la structure demandee. " + str(e))
                            return redirect('bonCommandeSortie')
                        '''#if not fields[1] == "fk_BonCommandeSortie":
                        data_dict["idBonCommandeSortie"] = fields[0]
                        data_dict["Client"] = fields[1]
                        data_dict["Destinataire"] = fields[2]
                        data_dict["codeDestinataire"] = fields[3]
                        data_dict["Transporteur"] = fields[4]
                        data_dict["numeroCommande"] = fields[5]
                        data_dict["dateCommande"] = fields[6]
                        data_dict["source"] = fields[7]'''
                    else: # les try except me permettent de savoir ou et pour quel raison mes update or create retournent une erreur
                        try:
                            LigneBonCommandeSortie_pour_BonCommandeSortie.objects.update_or_create(
                                idLigneBonCommandeSortie=fields[0],
                                fk_BonCommandeSortie=BonCommandeSortie.objects.get(idBonCommandeSortie=fields[1]),
                                fk_Article=Article.objects.get(codeClient=fields[2]),
                                quantiteProduitCommande=fields[4], #FLAG ERROR
                                quantiteProduitCommandestats=fields[4], #données qui sert a re-calculeor
                                priorite=fields[5], #données qui sert a la priorité
                            )
                            messages.success(request,"Succès -> Donnees du Csv ont ete ajoutees aux  tarifs")
                        except Exception as e:
                            messages.warning(request," Votre fichier n'est pas conforme à la structure demandee mauvais update ou create de bcs. " + str(e))
                            return redirect('bonCommandeSortie')
                        '''
                        #if not fields[1] == "﻿idLigneBonCommandeSortie":
                            #messages.error(request,"Unable to upload file Bad Keys0 .")
                            #return HttpResponseRedirect(reverse("bonCommandeSortie"))
                        data_dict["idLigneBonCommandeSortie"] = fields[0]
                        data_dict["fk_BonCommandeSortie"] = fields[1]
                        data_dict["Article"] = fields[2]
                        data_dict["designation"] = fields[3]
                        data_dict["quantiteProduitCommande"] = fields[4]
                        data_dict["priorite"] = fields[5]
                        data_dict["termine"] = fields[6]
                        data_dict["source"] = fields[7]'''
                print (data_dict)
                #Ici detecté le parsgage si parsage du CSV mauvais passé a l'exception
    except Exception as e:
        '''logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))'''
        messages.error(request,"Unable to upload file. " + repr(e))
    messages.success(request,"Files uplodade with no problem")

    #je fais un check de répartition des colis non expédié ||| Je Fais la répartition après avoir upload mon csv avec succès
    colis = Colis.objects.all().order_by("datePeremption", "fk_UniteManutentionEntree", "fk_Article", "-quantiteProduit") #Je recup la liste de colis, ordonnée par date peremption, umentree, article, et quantiteproduit decroissant
    lbc = LigneBonCommandeSortie_pour_BonCommandeSortie.objects.all().order_by("-priorite") #Je recup la liste de colis, ordonnée par la case priorite decroissante
    nombrecolisf = 0
    for items in colis:
        if items.emplacementConfirme == "0":
            print(items.quantiteProduit)
            try:
                if items.fk_UniteManutentionSortie == None:
                    for mylbc in lbc:
                        if mylbc.termine != 1:
                            if int(mylbc.quantiteProduitALivrer) - int(mylbc.quantiteProduitCommandestats) < 0:
                                if mylbc.fk_Article == items.fk_Article:
                                    print ("GG FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") #article correspondant a la ligne bon commande trouver dans les articles
                                    print (mylbc.quantiteProduitCommandestats + " !!!!!!! " + items.quantiteProduit)
                                    print ("Colis ! " + items.idColis) #article correspondant a la ligne bon commande trouver dans les articles
                                    if int(mylbc.quantiteProduitCommandestats) >= int(items.quantiteProduit): #verif que ça valeur du colis est tjr + petite que demander
                                        print ("GG2 FOUND  !!!!!!!!!!!!!!!!!!" + mylbc.quantiteProduitCommandestats + " and " + mylbc.quantiteProduitLivre)
                                        #if int(mylbc.quantiteProduitCommandestats) >= int(mylbc.quantiteProduitLivre): #verif que la ligne a encore besoin d'un colis en comparant ce qui a été donné a ce qui doit être donné
                                        print (mylbc.quantiteProduitLivre +" + " + items.quantiteProduit + " <= " + mylbc.quantiteProduitCommandestats)
                                            #Maintenant je dois sortir de le colis dans une Ums adéquate donc celle du bon de commande mylbc actuelle mais je dois vérifié que si je rajoute 1 colis je dépasse pas
                                            #if (int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit)) < int(mylbc.quantiteProduitCommandestats): Quand je fais mes checks de sécurité ça bug !
                                        items.fk_UniteManutentionSortie = UniteManutentionSortie.objects.get(fk_BonCommandeSortie=mylbc.fk_BonCommandeSortie)
                                        mylbc.quantiteProduitCommandestats = str(int(mylbc.quantiteProduitCommandestats) - int(items.quantiteProduit))
                                        mylbc.quantiteProduitLivre = str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit))
                                        mylbc.quantiteColisLivre = str(int(mylbc.quantiteColisLivre) + int(1))
                                        mylbc.save()
                                        items.save()
                                        print ("LBC CHANGED")
                                        nombrecolisf += 1
                                        break
                                        #else:
                                        #print (str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit)) + " Not changed quantite " + mylbc.quantiteProduitCommandestats)
                            else:
                                    print ("NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    #items.save()
            except Exception as e:
                print("error1x -- " + str(e))
    print ("So i had " + str(nombrecolisf) + " colis placed !")
    return HttpResponseRedirect(reverse("bonCommandeSortie"))

class bonCommandeSortieadd(ListView):
    template_name = "bonCommandeSortieadd.html"

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
            'bons' : BonCommandeSortie.objects.all(),
            'cli' : Client.objects.all(),
            'des' : Destinataire.objects.all(),
            'trans' : Transporteur.objects.all(),
            'settings' : menuimages.objects.all(),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

class bonCommandeSortiemodify(ListView):
    template_name = "bonCommandeSortiemodify.html"

    def termin(request):
        if request.method == 'POST':
            lbcs = LigneBonCommandeSortie_pour_BonCommandeSortie.objects.get(idLigneBonCommandeSortie=request.POST.get('idbcs'))
            if lbcs.termine == "0":
                lbcs.termine = "1"
            else:
                lbcs.termine = "0"
            lbcs.save()
            print ("LBCS OK ! " + request.POST.get('idbcs') + " " + lbcs.termine)
            return HttpResponse("Good access !")
        return HttpResponse("No access there !")

    def creebonlivraisonsortie(request): #c'est ici que le bouton "crée bl sorties" renvoi
        if request.method == 'POST':
            showlist = [request.POST.get('idbcs'), request.POST.get('transporteur'),
                        request.POST.get('destinataire')]
            print ("there " + showlist[0])

            ums = UniteManutentionSortie.objects.all()
            bcs = BonCommandeSortie.objects.all()
            umsopen = 0
            for myums in ums:
                if myums.fk_BonCommandeSortie.idBonCommandeSortie == showlist[0]:
                    print ("found good ums linked to this bcs now check if it is an 'open' one")
                    if myums.dateFermeture != "0" or myums.dateFermeture != "" and myums.fk_BonLivraisonSortie is None and myums.dateExpedition == "0" or myums.dateExpedition == "":
                        print ("this Ums is open")
                        #grace a ça je crée un bl car il y a au moins 1 ums ouvert
                        umsopen += 1
                    else:
                        print ("this Ums is closed " + myums.dateFermeture)
                #else:
                    #print ("Not found ums not linked to this bcs")
            blsid = 0
            if umsopen != 0:
                bls = BonLivraisonSortie()
                allbls = BonLivraisonSortie.objects.all()
                blsid = 0
                for mybls in allbls:
                    if blsid < int(mybls.idBonLivraisonSortie):
                        blsid = int(mybls.idBonLivraisonSortie)
                blsid = blsid + 1
                bls.idBonLivraisonSortie = str(blsid)
                bls.fk_BonCommandeSortie = BonCommandeSortie.objects.get(idBonCommandeSortie = showlist[0])
                bls.fk_LettreVoitureSortie = None
                bls.save()
                for myums in ums:
                    if myums.fk_BonCommandeSortie.idBonCommandeSortie == showlist[0]:
                        print ("found good ums linked to this bcs now check if it is an 'open' one")
                        if myums.dateFermeture != "0" or myums.dateFermeture != "" and myums.fk_BonLivraisonSortie is None and myums.dateExpedition == "0" or myums.dateExpedition == "":
                            myums.fk_BonLivraisonSortie = BonLivraisonSortie.objects.get(idBonLivraisonSortie=bls.idBonLivraisonSortie)
                            myums.dateExpedition = time.strftime("%Y-%m-%d")
                            myums.save()
                #vue que j'ai crée le bl sortie adéquat et que je lui ai donnée un um sortie ouvert et pas fermée et non expédiée je vais faire les lignes de ce bls maintenant
                col = Colis.objects.all()
                umsortie = UniteManutentionSortie.objects.all()
                art = Article.objects.all()
                try:
                    arrayofname = []
                    arrayofcolis = []
                    arrayofquantiteproduit = [] #c'est compliqué d'utilisé des dictionnaires avec 2 profondeurs, donc je crée 3 arrays qui stock 1 donnée chacuns
                    for colis in col:
                        for items in umsortie:
                            if colis.fk_UniteManutentionSortie is not None:
                                if colis.fk_UniteManutentionSortie.idUniteManutentionSortie == items.idUniteManutentionSortie:
                                    if items.fk_BonLivraisonSortie is not None:
                                        if items.fk_BonLivraisonSortie.idBonLivraisonSortie == bls.idBonLivraisonSortie:
                                            for article in art:
                                                if article.idArticle == colis.fk_Article.idArticle:
                                                    foundarticle = 0
                                                    idx = 0
                                                    while idx < len(arrayofname):
                                                        if arrayofname[idx] == colis.fk_Article: #je gère ici si l'article a déjà été trouver ou pas, si il existe je mets direct la quantité dedans
                                                            foundarticle = 1
                                                            arrayofquantiteproduit[idx] += int(colis.quantiteProduit)
                                                            arrayofcolis[idx] += 1
                                                        idx += 1
                                                    if foundarticle == 0:
                                                        arrayofname.append(colis.fk_Article)
                                                        arrayofquantiteproduit.append(int(colis.quantiteProduit))
                                                        arrayofcolis.append(1)
                                                        foundarticle = 1
                    idx = 0
                    alllignebls = LigneBonLivraisonSortie_pour_BonLivraisonSortie.objects.all()
                    art = Article.objects.all()
                    while idx < len(arrayofname):
                        id = 0
                        for lbls in alllignebls:
                            if id < int(lbls.idLigneBonLivraisonSortie):
                                id = int(lbls.idLigneBonLivraisonSortie)
                        id += 1
                        lignebls = LigneBonLivraisonSortie_pour_BonLivraisonSortie()
                        lignebls.idLigneBonLivraisonSortie = str(id)
                        lignebls.fk_Article = None
                        lignebls.fk_BonLivraisonSortie = None
                        for items in art:
                            print("so " + str(items.designationClient) + "X " + str(arrayofname[idx]) + "X")
                            if str(items.designationClient) == str(arrayofname[idx]):
                                print("good")
                                lignebls.fk_Article = items
                        if lignebls.fk_Article == None:
                            return HttpResponse("error1 !")
                        lignebls.fk_BonLivraisonSortie = bls
                        lignebls.quantiteProduit = str(arrayofquantiteproduit[idx])
                        lignebls.quantiteColis = str(arrayofcolis[idx])
                        lignebls.save()
                        print("name == " + str(arrayofname[idx]))
                        print("qteprod == " + str(arrayofquantiteproduit[idx]))
                        print("colisnbr == " + str(arrayofcolis[idx]))
                        idx += 1
                except Exception as e:
                    print ("Error " + str(e))
                    bls.delete()
                '''
                '{% for colis in col %}'
                    '{% for items in umentree %}'
                    '{% if colis.fk_UniteManutentionEntree|safe == items.idUniteManutentionEntree|safe %}'
                    '{% if items.fk_BonLivraisonEntree.idBonLivraisonEntree == id %}'
                    '{% for article in art %}'
                    '{% if article.idArticle == colis.fk_Article.idArticle %}'
                    foundarticle = 0;
                    for (var idx = 0; idx != arr.length; idx++) {
                    if (arr[idx].name == '{{ colis.fk_Article|safe }}') {//je gère ici si l'article a déjà été trouver ou pas, si il existe je mets direct la quantité dedans
                    foundarticle = 1;
                    arr[idx].quantiteproduit += parseInt('{{ colis.quantiteProduit|safe }}');
                    arr[idx].colis += 1;
                    }
                    }
                    if (foundarticle == 0) {
                    arr.push({name : '{{ colis.fk_Article|safe }}',
                                     quantiteproduit : parseInt('{{ colis.quantiteProduit|safe }}'),
                                                       colis : 1});
                    foundarticle = 1;
                    }
                    '{% endif %}'
                    '{% endfor %}'
                    /*for (var idx = 0; idx != arr.length; idx++) {
                    $('#tabblbody').last('tr').find('td').eq(1).find('select').append(new Option(, )); //rempli le code fournisseur une fois le colis trouvé
                    $("#iddesif").append(new Option("{{ colis.id|safe }}", "{{ colis.id|safe }}"));
                    }*/
                    '{% endif %}'
                    '{% endif %}'
                    '{% endfor %}'
                    '{% endfor %}'
                '''
            return HttpResponse("Good access !")
        return HttpResponse("No access there !")

    def recalcule(request):
        if request.method == 'POST':
            showlist = [request.POST.get('idbcs'), request.POST.get('codecli'),
                        request.POST.get('desicl'), request.POST.get('qtecom'),
                        request.POST.get('qtecol'), request.POST.get('qteatt'),
                        request.POST.get('diff'), request.POST.get('idligne')]

            print (showlist[0] + showlist[1] + showlist[2] +  showlist[3] +  showlist[4] + showlist[5] + showlist[6])
            try:
                go = LigneBonCommandeSortie_pour_BonCommandeSortie.objects.get(
                    idLigneBonCommandeSortie=showlist[7],
                   )
                if showlist[6]:
                    if int(showlist[6]) < 0:
                        if int(go.quantiteProduitCommandestats) - int(showlist[6]) > 0:
                            showlist[6] = str(abs(int(showlist[6])))
                            print("there " + showlist[6])
                            go.quantiteProduitCommandestats = str(int(showlist[6]))
                            #je libère les colis qui doivent l'être je "réduits" la quantité attribué manuellement dans le template
                            colis = Colis.objects.all().order_by("datePeremption", "fk_UniteManutentionEntree", "fk_Article", "quantiteProduit") #Je recup la liste de colis, ordonnée par date peremption, umentree, article, et quantiteproduit decroissant
                            while int(go.quantiteProduitLivre) > int(go.quantiteProduitCommandestats):
                                for items in colis:
                                    if items.fk_UniteManutentionSortie and \
                                            items.fk_Article.designationClient == showlist[2]:
                                        if str(items.fk_UniteManutentionSortie.fk_BonCommandeSortie) == str(showlist[0]):
                                            if int(go.quantiteProduitLivre) > int(showlist[5]):
                                                #print ("found colis to free ====! there ! " + str(items.fk_UniteManutentionSortie.fk_BonCommandeSortie) + "  " + str(showlist[0]))
                                                print ("remove colis / " + go.quantiteProduitLivre + "  / " + go.quantiteProduitCommandestats)
                                                go.quantiteColisLivre = str(int(go.quantiteColisLivre) - 1)
                                                go.quantiteProduitLivre = str(int(go.quantiteProduitLivre) - int(items.quantiteProduit))
                                                go.quantiteProduitCommandestats = str(int(go.quantiteProduitLivre))
                                                go.quantiteProduitALivrer = str(int(showlist[5]))
                                                items.fk_UniteManutentionSortie = None
                                                '''newcolis = Colis()
                                                newcolis.idColis = items.idColis
                                                newcolis.fk_UniteManutentionEntree = items.fk_UniteManutentionEntree
                                                newcolis.fk_UniteManutentionSortie = None
                                                newcolis.fk_Article = items.fk_Article
                                                newcolis.fk_litige = items.fk_litige
                                                newcolis.fk_LitigeDecision = items.fk_LitigeDecision
                                                newcolis.numeroLot = items.numeroLot
                                                newcolis.c_nom = items.c_nom
                                                newcolis.c_nomCompte = items.c_nomCompte
                                                newcolis.c_horodatage = items.c_horodatage
                                                newcolis.m_nom = items.m_nom
                                                newcolis.m_nomCompte = items.m_nomCompte
                                                newcolis.m_horodatage = items.m_horodatage
                                                newcolis.fk_ZoneDepot = items.fk_ZoneDepot
                                                newcolis.emplacementConfirme = items.emplacementConfirme
                                                newcolis.datePeremption = items.datePeremption
                                                newcolis.quantiteProduit = items.quantiteProduit
                                                newcolis.colle = items.colle
                                                newcolis.numerotation = items.numerotation
                                                items.delete()
                                                newcolis.save()'''
                                                items.save()
                                                go.save()
                                                #break
                            return HttpResponse("yes !")
            except LigneBonCommandeSortie_pour_BonCommandeSortie.DoesNotExist:
                    go = None
            #trie de sortie
            '''colis = Colis.objects.all().order_by("datePeremption", "fk_UniteManutentionEntree", "fk_Article", "-quantiteProduit") #Je recup la liste de colis, ordonnée par date peremption, umentree, article, et quantiteproduit decroissant
            lbc = LigneBonCommandeSortie_pour_BonCommandeSortie.objects.all().order_by("-priorite") #Je recup la liste de colis, ordonnée par la case priorite decroissante
            nombrecolisf = 0
            for items in colis:
                print(items.quantiteProduit)
                try:
                    if items.fk_UniteManutentionSortie == None:
                        for mylbc in lbc:
                            if int(mylbc.quantiteProduitALivrer) - int(mylbc.quantiteProduitCommandestats) < 0:
                                if mylbc.fk_Article == items.fk_Article:
                                    print ("GG FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") #article correspondant a la ligne bon commande trouver dans les articles
                                    print (mylbc.quantiteProduitCommandestats + " !!!!!!! " + items.quantiteProduit)
                                    print ("Colis ! " + items.idColis) #article correspondant a la ligne bon commande trouver dans les articles
                                    if int(mylbc.quantiteProduitCommandestats) >= int(items.quantiteProduit): #verif que ça valeur du colis est tjr + petite que demander
                                        print ("GG2 FOUND  !!!!!!!!!!!!!!!!!!" + mylbc.quantiteProduitCommandestats + " and " + mylbc.quantiteProduitLivre)
                                        #if int(mylbc.quantiteProduitCommandestats) >= int(mylbc.quantiteProduitLivre): #verif que la ligne a encore besoin d'un colis en comparant ce qui a été donné a ce qui doit être donné
                                        print (mylbc.quantiteProduitLivre +" + " + items.quantiteProduit + " <= " + mylbc.quantiteProduitCommandestats)
                                        #Maintenant je dois sortir de le colis dans une Ums adéquate donc celle du bon de commande mylbc actuelle mais je dois vérifié que si je rajoute 1 colis je dépasse pas
                                        #if (int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit)) < int(mylbc.quantiteProduitCommandestats): Quand je fais mes checks de sécurité ça bug !
                                        items.fk_UniteManutentionSortie = UniteManutentionSortie.objects.get(fk_BonCommandeSortie=mylbc.fk_BonCommandeSortie)
                                        mylbc.quantiteProduitCommandestats = str(int(mylbc.quantiteProduitCommandestats) - int(items.quantiteProduit))
                                        mylbc.quantiteProduitLivre = str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit))
                                        mylbc.quantiteColisLivre = str(int(mylbc.quantiteColisLivre) + int(1))
                                        mylbc.save()
                                        items.save()
                                        print ("LBC CHANGED")
                                        nombrecolisf += 1
                                        break
                                        #else:
                                        #print (str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit)) + " Not changed quantite " + mylbc.quantiteProduitCommandestats)
                            else:
                                print ("NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        #items.save()
                except Exception as e:
                    print("error1 -- " + str(e))
            print ("So i had " + str(nombrecolisf) + " colis placed !")''' #je ne dois aps trié "ici" mais via le button dans la pages des unite manutention entree!
        return HttpResponse("No access there !")

    def get(self, request):
        context = {
            'bcs' : BonCommandeSortie.objects.all(),
            'bls' : BonLivraisonSortie.objects.all(),
            'ums' : UniteManutentionSortie.objects.all(),
            'lbcs' : LigneBonCommandeSortie_pour_BonCommandeSortie.objects.all(),
            'trans' : Transporteur.objects.all(),
            'dest' : Destinataire.objects.all(),
            'cli' : Client.objects.all(),
            'id' :request.GET.get('id'),
            'settings' : menuimages.objects.all(),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

#c'est le bon de sortie pour les commande

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#ici fonction de trie pour les colis a -> tier vers les bcs qui ont des lignes encore ouvertes

def sortcolis(request):
    if request.method == 'POST':
        ume = UniteManutentionEntree.objects.get(idUniteManutentionEntree=request.POST.get('id'))
        colis = Colis.objects.all().order_by("datePeremption", "fk_UniteManutentionEntree", "fk_Article", "-quantiteProduit") #Je recup la liste de colis, ordonnée par date peremption, umentree, article, et quantiteproduit decroissant
        lbc = LigneBonCommandeSortie_pour_BonCommandeSortie.objects.all().order_by("-priorite") #Je recup la liste de colis, ordonnée par la case priorite decroissante
        bcs = BonCommandeSortie.objects.all()
        ums = UniteManutentionSortie.objects.all()
        nombrecolisf = 0
        for items in colis:
            if items.emplacementConfirme == "0":
                if items.fk_UniteManutentionEntree.idUniteManutentionEntree == ume.idUniteManutentionEntree:
                    print ("11") #article correspondant a la ligne bon commande trouver dans les articles
                    print(items.quantiteProduit)
                    try:
                        if not items.fk_UniteManutentionSortie:
                            print ("22")
                            for mylbc in lbc:
                                if mylbc.termine == "0":
                                    if int(mylbc.quantiteProduitALivrer) - int(mylbc.quantiteProduitCommandestats) < 0:
                                        if mylbc.fk_Article == items.fk_Article:
                                            print ("333") #article correspondant a la ligne bon commande trouver dans les articles
                                            print (mylbc.quantiteProduitCommandestats + " !!!!!!! " + items.quantiteProduit)
                                            print ("Colis ! " + items.idColis) #article correspondant a la ligne bon commande trouver dans les articles
                                            if int(mylbc.quantiteProduitCommandestats) >= int(items.quantiteProduit): #verif que ça valeur du colis est tjr + petite que demander
                                                print ("/// " + mylbc.quantiteProduitCommandestats + " and " + mylbc.quantiteProduitLivre)
                                                #if int(mylbc.quantiteProduitCommandestats) >= int(mylbc.quantiteProduitLivre): #verif que la ligne a encore besoin d'un colis en comparant ce qui a été donné a ce qui doit être donné
                                                print (mylbc.quantiteProduitLivre + " + " + items.quantiteProduit + " <= " + mylbc.quantiteProduitCommandestats)
                                                #Maintenant je dois sortir de le colis dans une Ums adéquate donc celle du bon de commande mylbc actuelle
                                                #if (int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit)) < int(mylbc.quantiteProduitCommandestats): plus besoin!
                                                #if UniteManutentionSortie.objects.get(fk_BonCommandeSortie=mylbc.fk_BonCommandeSortie).dateFermeture == "0": #l'ums ne doit pas être fermé, soit il est à 0
                                                nombrecolisf = 0
                                                for myums in ums:
                                                    if myums.fk_BonCommandeSortie.idBonCommandeSortie == mylbc.fk_BonCommandeSortie.idBonCommandeSortie:
                                                        if myums.dateFermeture == "0" or myums.dateFermeture == "":
                                                            items.fk_UniteManutentionSortie = myums
                                                            mylbc.quantiteProduitCommandestats = str(int(mylbc.quantiteProduitCommandestats) - int(items.quantiteProduit))
                                                            mylbc.quantiteProduitLivre = str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit))
                                                            mylbc.quantiteColisLivre = str(int(mylbc.quantiteColisLivre) + int(1))
                                                            mylbc.save()
                                                            items.save()
                                                            #sinon je dois crée un "ums" et relancer l'algo
                                                            print ("LBC CHANGED")
                                                            nombrecolisf += 1
                                                        else:
                                                            print("nope wtf " + myums.dateFermeture)
                                                if nombrecolisf == 0:
                                                    #print("there create !" + str(mylbc.fk_BonCommandeSortie))
                                                    go = UniteManutentionSortie()
                                                    try:
                                                        go.idUniteManutentionSortie = str(UniteManutentionSortie.objects.latest('idUniteManutentionSortie'))
                                                        go.idUniteManutentionSortie = str(int(go.idUniteManutentionSortie) + int(1))
                                                    except UniteManutentionSortie.DoesNotExist:
                                                        go.idUniteManutentionSortie = str(1)
                                                    go.fk_BonCommandeSortie = mylbc.fk_BonCommandeSortie
                                                    go.fk_BonLivraisonSortie = None
                                                    go.dateOuverture = time.strftime("%Y-%m-%d")
                                                    go.save()
                                                    items.fk_UniteManutentionSortie = go
                                                    #print("there create !" + str(go.idUniteManutentionSortie))
                                                    mylbc.quantiteProduitCommandestats = str(int(mylbc.quantiteProduitCommandestats) - int(items.quantiteProduit))
                                                    mylbc.quantiteProduitLivre = str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit))
                                                    mylbc.quantiteColisLivre = str(int(mylbc.quantiteColisLivre) + int(1))
                                                    mylbc.save()
                                                    items.save()
                                                    nombrecolisf += 1
                                                    print ("there i need to recreat a UMS")
                                                #break
                                                #else:
                                                #print (str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit)) + " Not changed quantite " + mylbc.quantiteProduitCommandestats)
                                    else:
                                        print ("NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            #items.save()
                    except Exception as e:
                        print("error1x -- " + str(e))
        print ("So i had " + str(nombrecolisf) + " colis placed !")
        return HttpResponse("good !")
    return HttpResponse("No Authorized Access !")

def sortOnecolis(request):
    if request.method == 'POST':
        ume = UniteManutentionEntree.objects.get(idUniteManutentionEntree=request.POST.get('umeid'))
        items = Colis.objects.get(idColis=request.POST.get('id'))
        lbc = LigneBonCommandeSortie_pour_BonCommandeSortie.objects.all().order_by("-priorite") #Je recup la liste de colis, ordonnée par la case priorite decroissante
        bcs = BonCommandeSortie.objects.all()
        ums = UniteManutentionSortie.objects.all()
        nombrecolisf = 0
        try:
            if not items.fk_UniteManutentionSortie:
                print(items.quantiteProduit)
                for mylbc in lbc:
                    if mylbc.termine == "0":
                        if int(mylbc.quantiteProduitALivrer) - int(mylbc.quantiteProduitCommandestats) < 0:
                            if mylbc.fk_Article == items.fk_Article:
                                if int(mylbc.quantiteProduitCommandestats) >= int(items.quantiteProduit): #verif que ça valeur du colis est tjr + petite que demander
                                    nombrecolisf = 0
                                    for myums in ums:
                                        if myums.fk_BonCommandeSortie.idBonCommandeSortie == mylbc.fk_BonCommandeSortie.idBonCommandeSortie:
                                            if myums.dateFermeture == "0" or myums.dateFermeture == "":
                                                articledestinataire = Article_Destinataire_pour_Article.objects.all()
                                                today = datetime.now()
                                                nombrecolisf += 1
                                                for arpd in articledestinataire:
                                                    noarticledestinataire = 0
                                                    if arpd.fk_Destinataire == mylbc.fk_BonCommandeSortie.fk_Destinataire:
                                                        print("Destinator found ! " + arpd.delaiPeremption + " " + str(today) + " diff " + str((datetime.strptime(items.datePeremption, "%Y-%m-%d") - today).days))
                                                        mydateitem = datetime.strptime(items.datePeremption, "%Y-%m-%d")
                                                        mydate = str((mydateitem - today).days)
                                                        print("her " + str(mydate) + " delai i got " + arpd.delaiPeremption)
                                                        if int(mydate) >= int(arpd.delaiPeremption):
                                                            print("good if")
                                                            articledestinataire = 1
                                                            break
                                                if articledestinataire == 1: #date de peremption personalisé ok
                                                    print("In inf " + str(mydate) + " . " + str(mylbc.fk_Article.delaiPeremption))
                                                    items.fk_UniteManutentionSortie = myums
                                                    mylbc.quantiteProduitCommandestats = str(int(mylbc.quantiteProduitCommandestats) - int(items.quantiteProduit))
                                                    mylbc.quantiteProduitLivre = str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit))
                                                    mylbc.quantiteColisLivre = str(int(mylbc.quantiteColisLivre) + int(1))
                                                    mylbc.save()
                                                    items.save()
                                                    print ("LBC CHANGED 1")
                                                else: #ici pas de date perso on prend la date par "défaut"
                                                    if mylbc.fk_Article.delaiPeremption != "" or mylbc.fk_Article.delaiPeremption != "0":
                                                        mydateitem = datetime.strptime(items.datePeremption, "%Y-%m-%d")
                                                        mydate = str((mydateitem - today).days)
                                                        print("her " + str(mydate) + " delai i got " + mylbc.fk_Article.delaiPeremption)
                                                        if int(mydate) >= int(mylbc.fk_Article.delaiPeremption):
                                                            items.fk_UniteManutentionSortie = myums
                                                            mylbc.quantiteProduitCommandestats = str(int(mylbc.quantiteProduitCommandestats) - int(items.quantiteProduit))
                                                            mylbc.quantiteProduitLivre = str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit))
                                                            mylbc.quantiteColisLivre = str(int(mylbc.quantiteColisLivre) + int(1))
                                                            mylbc.save()
                                                            items.save()
                                                            print ("LBC CHANGED 2")
                                                        else:
                                                            print("DLUO ISSUE " + items.idColis)
                                            else:
                                                print("nope")
                                    if nombrecolisf == 0:
                                        go = UniteManutentionSortie()
                                        try:
                                            go.idUniteManutentionSortie = str(UniteManutentionSortie.objects.latest('idUniteManutentionSortie'))
                                            go.idUniteManutentionSortie = str(int(go.idUniteManutentionSortie) + int(1))
                                        except UniteManutentionSortie.DoesNotExist:
                                            go.idUniteManutentionSortie = str(1)
                                        go.fk_BonCommandeSortie = mylbc.fk_BonCommandeSortie
                                        go.fk_BonLivraisonSortie = None
                                        go.dateOuverture = time.strftime("%Y-%m-%d")
                                        go.save()
                                        items.fk_UniteManutentionSortie = go
                                        #print("there create !" + str(go.idUniteManutentionSortie))
                                        mylbc.quantiteProduitCommandestats = str(int(mylbc.quantiteProduitCommandestats) - int(items.quantiteProduit))
                                        mylbc.quantiteProduitLivre = str(int(mylbc.quantiteProduitLivre) + int(items.quantiteProduit))
                                        mylbc.quantiteColisLivre = str(int(mylbc.quantiteColisLivre) + int(1))
                                        mylbc.save()
                                        items.save()
                                        nombrecolisf += 1
                                        print ("there i need to recreat a UMS")
                            else:
                                print ("NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        except Exception as e:
            print("error1x -- " + str(e))
        #print ("So i had " + str(nombrecolisf) + " colis placed !")
        return HttpResponse("good !")
    return HttpResponse("No Authorized Access !")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#ici je crée les lettre de voiture entree
class lettrevoitureentreeadd(ListView):
    template_name = "lettrevoitureentreeadd.html"   #template pour crée une LV.entree

    def create(request): #fonction qui crée une L.V entree via les donnée rempli dans le template html
        if request.method == 'POST': #je vérifie que la requête reçus est bien une reqête POST
            lve = LettreVoitureEntree.objects.all() #je recupère toutes les entrées que contient LettreVoitureEntree
            trans = Transporteur.objects.all() # je fais pareil pour les entrées Transporteur
            showlist = [request.POST.get('id'), request.POST.get('dater'),
                        request.POST.get('numr'), request.POST.get('qpalette'),
                        request.POST.get('transp'), request.POST.get('qcolis'),
                        request.POST.get('quantitecolrecla'), request.POST.get('quantitepalrecla'),             #ici je recois les donnée reçus via la requete ajax en js
                        request.POST.get('comrecla'),]
            lettre = LettreVoitureEntree()
            for items in trans:
                if items.nom == showlist[4]:
                    lettre.fk_Transporteur = items #si je trouve un Transporteur qui a le même nom que celui choisis dans le template, je rentre l'objet dans la clé Fk_Transporteur
            lettre.idLettreVoitureEntree = showlist[0] #je rentre l'id recus via ajax
            lettre.datereception = showlist[1]
            lettre.numerorecepisse = showlist[2]
            lettre.quantitepalette = showlist[3]
            lettre.quantitecolis = showlist[5]
            lettre.reclaquantitecolis = showlist[6]
            lettre.reclaquantitepalette = showlist[7]
            lettre.reclacomm = showlist[8]

            id = 0
            try:
                go = LettreVoitureEntree.objects.get(idLettreVoitureEntree=showlist[0])
                for mylve in lve:
                    if id < int(mylve.idLettreVoitureEntree):
                        id = int(mylve.idLettreVoitureEntree)
                id+=1
                lettre.idLettreVoitureEntree = str(id) #je gère que cet id est déjà prit
            except LettreVoitureEntree.DoesNotExist:
                '''ici je fais rien car il n'y a pas de "lve" avec un id déjà pris, donc je peux laisser le lve se faire save ;)'''
            lettre.save()   #quand toute les variables a modifié l'ont été je sauvegard mon "object" qui devient un nouvel enregistrement dans ma BDD
            if id == 0:
                return HttpResponse(showlist[0])    #retours pour signifier un succès
            else:
                return HttpResponse(str(id))    #retours pour signifier un succès
        return HttpResponse("No Authorized Access !")

    def get(self, request): #get équivaut a un "main" on lui envoi les ressource nécessaire a la completion de la page, par ex lve pourra être utiliser dans le template html
        context = {
            'lve' : LettreVoitureEntree.objects.all(),
            'four' : Fournisseur.objects.all(),
            'trans' : Transporteur.objects.all(),
            'settings' : menuimages.objects.all(),
            #'entreeligne' : LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class lettrevoitureentreemodify(ListView):
    template_name = "lettrevoitureentreemodify.html"

    def deletebl(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            ble = BonLivraisonEntree.objects.all()
            for items in ble:
                if items.idBonLivraisonEntree == showlist[0]:
                    items.delete()
            return HttpResponse("Delete successfull")
        return HttpResponse("No Authorized Access !")

    def createbl(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('trueid'),]
            bonle = BonLivraisonEntree()
            lve = LettreVoitureEntree.objects.all()
            bonle.idBonLivraisonEntree = showlist[1]
            bonle.fk_Client = None
            bonle.fk_Fournisseur = None
            bonle.fk_TypeZoneDepot = None
            for items in lve:
                if items.idLettreVoitureEntree == showlist[0]:
                    bonle.fk_LettreVoitureEntree = items #je parcours les LettreVoiturEentree pour trouver celui qui me sert a crée un bl
            bonle.fk_BonCommandeEntree = None
            bonle.fk_UniteManutentionEntree = None
            bonle.fk_Destinataire = None
            bonle.fk_ZoneDepot_pour_TypeZoneDepot = None
            bonle.save()
            return HttpResponse("Created !" + str(showlist[0]) + ' '+ str(showlist[1]))
        return HttpResponse("No Authorized Access !")

    def modify(request):
        if request.method == 'POST':
            lettre = LettreVoitureEntree.objects.get(idLettreVoitureEntree=request.POST['id'])
            trans = Transporteur.objects.all()
            showlist = [request.POST.get('id'), request.POST.get('dater'),
                        request.POST.get('numr'), request.POST.get('qpalette'),
                        request.POST.get('transp'), request.POST.get('qcolis'),
                        request.POST.get('quantitecolrecla'), request.POST.get('quantitepalrecla'),
                        request.POST.get('comrecla'),]
            for items in trans:
                if items.nom == showlist[4]:
                    lettre.fk_Transporteur = items
            lettre.idLettreVoitureEntree = showlist[0]
            lettre.datereception = showlist[1]
            lettre.numerorecepisse = showlist[2]
            lettre.quantitepalette = showlist[3]
            lettre.quantitecolis = showlist[5]
            lettre.reclaquantitecolis = showlist[6]
            lettre.reclaquantitepalette = showlist[7]
            lettre.reclacomm = showlist[8]
            lettre.save()
            #ble = BonLivraisonEntree.objects.get(idBonLivraisonEntree=request.POST['id'])
            #article.delete()
            return HttpResponse("Deleted !")
        return HttpResponse("No Authorized Access !")

    def upload_lvef(request):
        if request.method == 'POST':
            fichier = request.FILES.get('file', False)
            photo = request.FILES.get('photo', False)
            idinput = request.POST.get('idinput')
            lve = LettreVoitureEntree.objects.get(idLettreVoitureEntree=idinput)
            lve.fichier = None
            lve.fichier = fichier
            lve.photo = None
            lve.photo = photo
            lve.save()
            return redirect(reverse('lvemodify')+"?id="+lve.idLettreVoitureEntree) #ici on fait un "redirect" (qui va renvoyer vers une page) qui utilise reverse (reverse) qui permet d'utiliser le nom de l'url
        return HttpResponse("No Authorized Access !")

    def get(self, request):
        context = {
            'lve' : LettreVoitureEntree.objects.all(),
            'entree' : BonLivraisonEntree.objects.all(),
            #'entreeligne' : LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.all(),
            'four' : Fournisseur.objects.all(),
            'trans' : Transporteur.objects.all(),
            'id' :request.GET.get('id'),
            'settings' : menuimages.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class lettrevoitureentree(ListView):
    template_name = "lettrevoitureentree.html"

    def delete(request):
        if request.method == 'POST':
            lve = LettreVoitureEntree.objects.get(idLettreVoitureEntree=request.POST['id'])
            lve.delete()
            return HttpResponse("Deleted !")
        return HttpResponse("No Authorized Access !")

    def get(self, request):
        context = {
            'lve' : LettreVoitureEntree.objects.all(),
            'settings' : menuimages.objects.all(),
            #'entreeligne' : LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class bonLivraisonEntree(ListView):
    template_name = "bonLivraisonEntree.html"

    def delete(request): #fonction pour supprimer un B.L entree dans la page Bonlivraisonentree via les "X" sur la ligne des bl
        if request.method == 'POST':
            ble = BonLivraisonEntree.objects.get(idBonLivraisonEntree=request.POST['id'])
            ble.delete()
            return HttpResponse("Deleted !") #réponse renvoyer pour savoir si aucun problème
        return HttpResponse("No Authorized Access !") #retour a envoyé si une personne accède au lien directement hors les requete pré-établies

    def get(self, request):
        context = {
            'entree' : BonLivraisonEntree.objects.all(),
            'settings' : menuimages.objects.all(),
            #'entreeligne' : LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class bonLivraisonentreemodify(ListView):
    template_name = "bonlivraisonentreemodify.html"

    def left(request):
        if request.method == 'POST':
            before = request.POST['id']
            bl = BonLivraisonEntree.objects.get(idBonLivraisonEntree=request.POST['id'])

            for i in range(int(before)-1, 0, -1):
                try:
                    go = BonLivraisonEntree.objects.get(idBonLivraisonEntree=str(i))
                    return HttpResponse(i)
                except BonLivraisonEntree.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def right(request): #C'est grace a cette fontion que je peux aller a "droite" d'un BonLivraisonentree via le template Bonlivraisonentremodify
        if request.method == 'POST':
            my_total = BonLivraisonEntree.objects.count()
            after = request.POST['id']
            bl = BonLivraisonEntree.objects.get(idBonLivraisonEntree=request.POST['id'])
            mybl = BonLivraisonEntree.objects.all()
            id = 0
            for bl in mybl:
                if id < int(bl.idBonLivraisonEntree):
                    id = int(bl.idBonLivraisonEntree)
            print("id = " + str(id) + '\n')
            for i in range(int(after)+1, id+1, 1):
                try:
                    go = BonLivraisonEntree.objects.get(idBonLivraisonEntree=str(i))
                    return HttpResponse(i)
                except BonLivraisonEntree.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def createume(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]

            id = 0
            numum = 0
            for myume in UniteManutentionEntree.objects.all():
                if id < int(myume.idUniteManutentionEntree):
                    id = int(myume.idUniteManutentionEntree)
                if myume.fk_BonLivraisonEntree:
                    if myume.fk_BonLivraisonEntree.idBonLivraisonEntree == showlist[0]:
                        if numum  < int(myume.numero):
                            numum = int(myume.numero)
            numum = numum + 1
            id = id + 1
            ume = UniteManutentionEntree()
            ume.idUniteManutentionEntree = str(id)
            ume.numero = numum
            ume.fk_BonLivraisonEntree = BonLivraisonEntree.objects.get(idBonLivraisonEntree=showlist[0])
            ume.fk_ZoneDepot = None
            ume.save()
            return HttpResponse("Created !")
        return HttpResponse("No Authorized Access !")

    def deleteume(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            for myume in UniteManutentionEntree.objects.all():
                if myume.idUniteManutentionEntree == showlist[0]: #équivalent du "objects.get()" de django permet d'éviter de faire des try catch
                    myume.delete()
            return HttpResponse("delete ume successfull !")
        return HttpResponse("No Authorized Access !")

    def modify(request):
        if request.method == 'POST':
            ble = BonLivraisonEntree.objects.all()
            fourtype = Fournisseur.objects.all()
            cli = Client.objects.all()
            lveo = LettreVoitureEntree.objects.all()
            art = Article.objects.all()
            zne = TypeZoneDepot.objects.all()
            inzne = ZoneDepot_pour_TypeZoneDepot.objects.all()
            litiges = Destinataire.objects.all()
            foundcli = 0
            showlist = [request.POST.get('id'), request.POST.get('client'),
                        request.POST.get('fourtype'), request.POST.get('lettre'),
                        request.POST.get('zone'), request.POST.get('numerobl'),
                        request.POST.get('daterecep'), request.POST.get('quantitepale'),
                        request.POST.get('destinataireretour'), request.POST.get('zoneatt')]
            bonle = BonLivraisonEntree.objects.get(idBonLivraisonEntree=showlist[0])
            bonle.fk_Client = None
            bonle.fk_Fournisseur = None
            bonle.fk_TypeZoneDepot = None
            bonle.fk_LettreVoitureEntree = None
            bonle.fk_BonCommandeEntree = None
            bonle.fk_UniteManutentionEntree = None
            bonle.fk_Destinataire = None
            for items in cli:
                if showlist[1] == items.nom:
                    bonle.fk_Client = items
            for items in fourtype:
                if showlist[2] == items.nom:
                    bonle.fk_Fournisseur = items
            for items in lveo:
                if showlist[3] == items.idLettreVoitureEntree:
                    bonle.fk_LettreVoitureEntree = items
            bonle.numeroBonLivraison = showlist[5]
            bonle.dateReception = showlist[6]
            bonle.quantitePalette = showlist[7]
            for items in litiges:
                if showlist[8] == items.nom:
                    bonle.fk_Destinataire = items

            for items in inzne:
                if showlist[9] == items.nom:
                    #bonle.fk_TypeZoneDepot = items
                    print ("print "+ items.nom + "  et0  "+ showlist[9])
                    for initems in zne:
                        #print ("print !!!! "+ initems.nom + "  !!!!et  " + str(items.fk_TypeZoneDepot))
                        if initems.nom == items.fk_TypeZoneDepot.nom:
                            bonle.fk_TypeZoneDepot = initems

            inzone = ZoneDepot_pour_TypeZoneDepot.objects.all()
            for zone in inzone:
                if request.POST.get('zoneatt') == zone.nom:
                    bonle.fk_ZoneDepot_pour_TypeZoneDepot = zone
                if request.POST.get('zoneatt') == "":
                    bonle.fk_ZoneDepot_pour_TypeZoneDepot = None
            bonle.save()
            return HttpResponse("Created !")
        return HttpResponse("No Authorized Access !")

    def get(self, request):
        context = {
            'entree' : BonLivraisonEntree.objects.all(),
            'umentree' : UniteManutentionEntree.objects.all(),
            'col' : Colis.objects.all(),
            'art' : Article.objects.all(),
            'cli' : Client.objects.all(),
            'des' : Destinataire.objects.all(),
            'four' : Fournisseur.objects.all(),
            'typef': TypeFournisseur_pour_Fournisseur.objects.all(),
            'zoned': ZoneDepot_pour_TypeZoneDepot.objects.all(),
            #'lve' : LettreVoitureEntree.objects.all(),
            'entreeligne' : LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.all(),
            'id' :request.GET.get('id'),
            'settings' : menuimages.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

def upload_blef(request):
    fichier = request.FILES.get('file', False)
    photo = request.FILES.get('photo', False)
    idinput = request.POST.get('idinput')
    ble = BonLivraisonEntree.objects.get(idBonLivraisonEntree=idinput)
    ble.fichier = None
    ble.fichier = fichier
    ble.photo = None
    ble.photo = photo
    ble.save()
    return redirect(reverse('bonLivraisonEntreemodify')+"?id="+ble.idBonLivraisonEntree)
    #return reverse('bonLivraisonEntreemodify', kwargs={'pk': 5})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class bonLivraisonEntreeadd(ListView):
    template_name = "bonLivraisonEntreeadd.html"

    def create(request):
        if request.method == 'POST':
            ble = BonLivraisonEntree.objects.all()
            fourtype = Fournisseur.objects.all()
            cli = Client.objects.all()
            bonle = BonLivraisonEntree()
            lveo = LettreVoitureEntree.objects.all()
            art = Article.objects.all()
            zne = TypeZoneDepot.objects.all()
            inzne = ZoneDepot_pour_TypeZoneDepot.objects.all()
            litiges = Destinataire.objects.all()
            foundcli = 0
            id = 0
            showlist = [request.POST.get('id'), request.POST.get('client'),
                        request.POST.get('fourtype'), request.POST.get('lettre'),
                        request.POST.get('zone'), request.POST.get('numerobl'),
                        request.POST.get('daterecep'), request.POST.get('quantitepale'),
                        request.POST.get('destinataireretour'), request.POST.get('zoneatt')]
            '''for items in ble:
                if showlist[0] == items.idBonLivraisonEntree:
                    return HttpResponse("Ble aldready existing !")'''
            bonle.idBonLivraisonEntree = showlist[0]
            bonle.fk_Client = None
            bonle.fk_Fournisseur = None
            bonle.fk_TypeZoneDepot = None
            bonle.fk_ZoneDepot_pour_TypeZoneDepot = None
            bonle.fk_LettreVoitureEntree = None
            bonle.fk_BonCommandeEntree = None
            bonle.fk_UniteManutentionEntree = None
            bonle.fk_Destinataire = None
            for items in cli:
                if showlist[1] == items.nom:
                    bonle.fk_Client = items
                    #= items
                #for myzone in zne:
                #if showlist[4] == items.nom:
                #bonle.fk_TypeZone = items
            for items in fourtype:
                if showlist[2] == items.nom:
                    bonle.fk_Fournisseur = items
            for items in lveo:
                if showlist[3] == items.idLettreVoitureEntree:
                    bonle.fk_LettreVoitureEntree = items
            bonle.numeroBonLivraison = showlist[5]
            bonle.dateReception = showlist[6]
            bonle.quantitePalette = showlist[7]
            for items in litiges:
                if showlist[8] == items.nom:
                    bonle.fk_Destinataire = items
            for items in inzne:
                if showlist[9] == items.nom:
                    #bonle.fk_TypeZoneDepot = items
                    print ("print "+ items.nom + " e!!!!!!!!!t1 "+ showlist[9])
                    for initems in zne:
                        print ("print "+ initems.nom + " e!!!!!!!!!t "+ items.fk_TypeZoneDepot.nom)
                        if initems.nom == items.fk_TypeZoneDepot.nom:
                            bonle.fk_TypeZoneDepot = initems
            inzone = ZoneDepot_pour_TypeZoneDepot.objects.all()
            for zone in inzone:
                if request.POST.get('zoneatt') == zone.nom:
                    bonle.fk_ZoneDepot_pour_TypeZoneDepot = zone
                if request.POST.get('zoneatt') == "":
                    bonle.fk_ZoneDepot_pour_TypeZoneDepot = None
            id = 0
            try:
                go = BonLivraisonEntree.objects.get(idBonLivraisonEntree=showlist[0])
                for myble in ble:
                    if id < int(myble.idBonLivraisonEntree):
                        id = int(myble.idBonLivraisonEntree)
                id+=1
                bonle.idBonLivraisonEntree = str(id) #je gère que cet id est déjà prit
            except BonLivraisonEntree.DoesNotExist:
                '''ici je fais rien car il n'y a pas de "lve" avec un id déjà pris, donc je peux laisser le lve se faire save ;)'''
            bonle.save() #quand toute les variables a modifié l'ont été je sauvegard mon "object" qui devient un nouvel enregistrement dans ma BDD
            if id == 0:
                return HttpResponse(showlist[0])    #retours pour signifier un succès
            else:
                return HttpResponse(str(id))    #retours pour signifier un succès
            #return HttpResponse("Created !")
        return HttpResponse("No Authorized Access !")

    def createligne(request):
        if request.method == 'POST':
            ligne = LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.all()
            art = Article.objects.all()
            ble = BonLivraisonEntree.objects.all()
            showlist = [request.POST.get('id'), request.POST.get('lbid'),
                        request.POST.get('codefour'), request.POST.get('desicli'),
                        request.POST.get('quantiteprod'), request.POST.get('quantitecolis'),
                        request.POST.get('controle'), request.POST.get('termine'),
                        request.POST.get('commattendu'), request.POST.get('commrecus'),
                        request.POST.get('produitsrecu'), request.POST.get('colisrecu'),
                        request.POST.get('produitsalivrer'), request.POST.get('colisalivrer'),
                        request.POST.get('colislitigieux'), request.POST.get('produitslitgieux'),
                        request.POST.get('autrediffs'), request.POST.get('diffproduit'),
                        request.POST.get('diffnonexp')]
            '''if (showlist[1] == None):
                ligne_eble = LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.get(idLigneBonLivraisonEntree=showlist[1])
            else:
                ligne_eble = LigneBonLivraisonEntree_pour_BonLivraisonEntree()
                ligne_eble.idLigneBonLivraisonEntree = showlist[1]
                ligne_eble.fk_Article = None
                ligne_eble.fk_BonLivraisonEntree = None'''
            try:
                ligne_eble = LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.get(idLigneBonLivraisonEntree=showlist[1])
            except LigneBonLivraisonEntree_pour_BonLivraisonEntree.DoesNotExist:
                ligne_eble = LigneBonLivraisonEntree_pour_BonLivraisonEntree()
                ligne_eble.idLigneBonLivraisonEntree = showlist[1]
                ligne_eble.fk_Article = None
                ligne_eble.fk_BonLivraisonEntree = None
            for items in art:
                print(items.designationClient + "--" + showlist[3]+"X")
                if items.designationClient == showlist[3]:
                    ligne_eble.fk_Article = items
            for items in ble:
                if items.idBonLivraisonEntree == showlist[0]:
                    ligne_eble.fk_BonLivraisonEntree = items
            ligne_eble.controle = showlist[6]
            ligne_eble.quantiteColis = showlist[5]
            ligne_eble.quantiteColisAlivrer = showlist[13]
            ligne_eble.quantiteColisLitige = showlist[14]
            ligne_eble.quantiteColisRecu = showlist[11]
            ligne_eble.quantiteCommande = showlist[8]
            ligne_eble.quantiteCommandeRecue = showlist[9]
            ligne_eble.quantiteDifferenceAutre = showlist[16]
            ligne_eble.quantiteDifference = showlist[17]
            ligne_eble.quantiteDifferenceRestante = showlist[18]
            ligne_eble.quantiteProduit = showlist[4]
            ligne_eble.quantiteProduitAlivrer = showlist[12]
            ligne_eble.quantiteProduitLitige = showlist[15]
            ligne_eble.termine = showlist[7]
            ligne_eble.save()
            return HttpResponse("Ligne Bl Created !")
        return HttpResponse("No Authorized Access !")

    def deleteligne(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            try:
                ligne = LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.get(idLigneBonLivraisonEntree=showlist[0])
                ligne.delete()
                return HttpResponse("deleted !")
            except LigneBonLivraisonEntree_pour_BonLivraisonEntree.DoesNotExist:
                ligne = None
            return HttpResponse("error !")
        return HttpResponse("No Authorized Access !")

    def get(self, request):
        context = {
            'entree' : BonLivraisonEntree.objects.all(),
            'art' : Article.objects.all(),
            'cli' : Client.objects.all(),
            'des' : Destinataire.objects.all(),
            'four' : Fournisseur.objects.all(),
            'typef': TypeFournisseur_pour_Fournisseur.objects.all(),
            'zoned': ZoneDepot_pour_TypeZoneDepot.objects.all(),
            #'lve' : LettreVoitureEntree.objects.all(),
            'settings' : menuimages.objects.all(),
            'entreeligne' : LigneBonLivraisonEntree_pour_BonLivraisonEntree.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class bonLivraisonSortie(ListView):
    template_name = "bonLivraisonSortie.html"

    def get(self, request):
        context = {
            'blsortie' : BonLivraisonSortie.objects.all(),
            'sortieligne' : LigneBonLivraisonSortie_pour_BonLivraisonSortie.objects.all(),
            'settings' : menuimages.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

class bonLivraisonSortiemodify(ListView):
    template_name = "bonLivraisonSortiemodify.html"

    def upload_blsf(request):
        if request.method == 'POST':
            fichier = request.FILES.get('file', False)
            idinput = request.POST.get('idinput')
            bls = BonLivraisonSortie.objects.get(idBonLivraisonSortie=idinput)
            bls.fichier = None
            if fichier:
                bls.fichier = fichier
            bls.save()
            print("gg fichier sauvegarder !!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(reverse('bonLivraisonSortiemodify')+"?id="+bls.idBonLivraisonSortie)
        return HttpResponse("No access authorized !")

    def get(self, request):
        context = {
            'sortie' : BonLivraisonSortie.objects.all(),
            'sortieligne' : LigneBonLivraisonSortie_pour_BonLivraisonSortie.objects.all(),
            'bcs' : BonCommandeSortie.objects.all(),
            'ums' : UniteManutentionSortie.objects.all(),
            'settings' : menuimages.objects.all(),
            'activate' : 'on',
            'id' : request.GET.get('id'),
            'cli' : Client.objects.all(),
            'dest' : Destinataire.objects.all(),
            'trans' : Transporteur.objects.all(),
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class bonLivraisonSortieadd(ListView):
    template_name = "bonLivraisonSortieadd.html"

    def get(self, request):
        context = {
            'sortie' :BonLivraisonSortie.objects.all().select_related('fk_BonCommandeSortie', 'fk_LettreVoitureSortie'),
            'sortieligne' :LigneBonLivraisonSortie_pour_BonLivraisonSortie.objects.all().select_related('fk_Article', 'fk_BonLivraisonSortie'),
            'settings' : menuimages.objects.all(),
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
        article = Article.objects.all()
        col = Colis.objects.all()
        ums = UniteManutentionSortie.objects.all()
        ume = UniteManutentionEntree.objects.all()

        for myarticle in article:
            myarticle.quantiteProduitStockComplet = 0
            myarticle.quantiteColisStockComplet = 0
            myarticle.quantiteProduitStockIncomplet = 0
            myarticle.quantiteColisStockIncomplet =  0
            myarticle.save()

        for items in col:
            for myarticle in article:
                #print("gggggggggggggggggg2")
                if items.fk_Article.designationClient == myarticle.designationClient: #je suis dans une "ligne" de colis ici, dedans je vais chercher dans les colis non expedié (umsortie) pour avoir le stock
                    for myume in ume:
                        if str(items.fk_UniteManutentionEntree) == myume.idUniteManutentionEntree:
                            if items.fk_UniteManutentionSortie == None:
                                if items.quantiteProduit == myarticle.quantiteColisStandard:
                                    if items.quantiteProduit == None:
                                        items.quantiteProduit = 0
                                    myarticle.quantiteProduitStockComplet += int(items.quantiteProduit)
                                    myarticle.quantiteColisStockComplet +=  1
                                    #print("gg2 " + str(myarticle.designationClient) + " gg")
                                    myarticle.save()
                                else:
                                    if items.quantiteProduit == None:
                                        items.quantiteProduit = 0
                                    #print("gg4 " + str(items.quantiteProduit) + " gg")
                                    myarticle.quantiteProduitStockIncomplet += int(items.quantiteProduit)
                                    myarticle.quantiteColisStockIncomplet +=  1
                                    #print("gg3 " + str(myarticle.designationClient) + " gg")
                                    myarticle.save()
                    #print(items.fk_Article.designationClient + "  " + items.idColis)
        context = {
            'art' : Article.objects.all(),
            'settings' : menuimages.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

class articleemplacement(ListView):
    template_name = "articleemplacement.html"

    def get(self, request):
        context = {
            'art' : Article.objects.all(),
            'zndp' : ZoneDepot_pour_TypeZoneDepot.objects.all(),
            'ume' : UniteManutentionEntree.objects.all(),
            'col' : Colis.objects.all(),
            'name' :request.GET.get('name'),
            'settings' : menuimages.objects.all(),
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

            article.fk_Fournisseur = None
            article.fk_TypeArticle = None

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
            'settings' : menuimages.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class articlemodify(ListView):
    template_name = "articlemodify.html"

    def updatedestinator(request):
        if request.method == 'POST':
            showlist = [request.POST.get('umcode'), request.POST.get('desti'),
                        request.POST.get('delai'), request.POST.get('idart'), request.POST.get('artdesid')]
            artdesall = Article_Destinataire_pour_Article.objects.all()
            id = 1
            for items in artdesall:
                if id < int(items.idArticle_Destinataire):
                    id = int(items.idArticle_Destinataire)
            id += 1
            try:
                articledpa = Article_Destinataire_pour_Article.objects.get(idArticle_Destinataire=showlist[4])
                print("found")
                try:
                    article = Article.objects.get(idArticle=showlist[3])
                    destinataire = Destinataire.objects.get(nom=showlist[1])
                    articledpa.fk_Article = article
                    articledpa.fk_Destinataire = destinataire
                    articledpa.delaiPeremption = showlist[2]
                    articledpa.save()
                except Article.DoesNotExist:
                    print ("error article issue check the \"id\" in your page !" + str(showlist[3]))
                except Destinataire.DoesNotExist:
                    print ("error destinator not found check the \"name\" of your destinator !" + str(showlist[1]))
            except Article_Destinataire_pour_Article.DoesNotExist:
                articledpa = Article_Destinataire_pour_Article()
                articledpa.idArticle_Destinataire = str(id)
                print("not found")
                try:
                    article = Article.objects.get(idArticle=showlist[3])
                    destinataire = Destinataire.objects.get(nom=showlist[1])
                    articledpa.fk_Article = article
                    articledpa.fk_Destinataire = destinataire
                    articledpa.delaiPeremption = showlist[2]
                    articledpa.save()
                except Article.DoesNotExist:
                    print ("error article issue check the \"id\" in your page !" + str(showlist[3]))
                except Destinataire.DoesNotExist:
                    print ("error destinator not found check the \"name\" of your destinator !" + str(showlist[1]))
            return HttpResponse("article modified !")
        return HttpResponse("Unauthorized page !")

    def deletedestinator(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            try:
                destiarticle = Article_Destinataire_pour_Article.objects.get(idArticle_Destinataire=showlist[0])
                destiarticle.delete()
            except Article_Destinataire_pour_Article.DoesNotExist:
                print ("error article issue check the \"id\" in your page !" + str(showlist[0]))
            return HttpResponse("article modified !")
        return HttpResponse("Unauthorized page !")

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

            article.fk_Fournisseur = None
            article.fk_TypeArticle = None

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
            'des' : Destinataire.objects.all(),
            'histoart ' : Article_historique_pour_Article.objects.all(),
            'four' : Fournisseur.objects.all(),
            'ardes' : Article_Destinataire_pour_Article.objects.all(),
            'settings' : menuimages.objects.all(),
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
            'settings' : menuimages.objects.all(),
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
            'settings' : menuimages.objects.all(),
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
            'settings' : menuimages.objects.all(),
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
            'settings' : menuimages.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class transporteuradd(ListView):
    template_name = "transporteuradd.html"

    def get(self, request):
        context = {
            'trans' :Transporteur.objects.all(),
            'settings' : menuimages.objects.all(),
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

    def left(request):
        if request.method == 'POST':
            before = request.POST['id']
            transporteur = Transporteur.objects.get(idTransporteur=request.POST['id'])
            for i in range(int(before)-1, 0, -1):
                try:
                    go = Transporteur.objects.get(idTransporteur=str(i))
                    return HttpResponse(i)
                except Transporteur.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def right(request):
        if request.method == 'POST':
            my_total = Transporteur.objects.count()
            after = request.POST['id']
            transporteur = Transporteur.objects.get(idTransporteur=request.POST['id'])

            trans = Transporteur.objects.all()
            id = 0
            for mytrans in trans:
                if id < int(mytrans.idTransporteur):
                    id = int(mytrans.idTransporteur)
            print("id = " + str(id))

            for i in range(int(after)+1, id+1, 1):
                try:
                    print("id = " + str(id))
                    go = Transporteur.objects.get(idTransporteur=str(i))
                    return HttpResponse(i)
                except Transporteur.DoesNotExist:
                    go = None
                print (i)
            return HttpResponse("fail")
        return HttpResponse("No Authorized Access !")

    def get(self, request):
        context = {
            'trans' :Transporteur.objects.all(),
            'name' :request.GET.get('name'),
            'id' :request.GET.get('id'),
            'settings' : menuimages.objects.all(),
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
            'settings' : menuimages.objects.all(),
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

            destinataire.departement = showlist[14]
            destinataire.adresseFacturation = showlist[15]
            destinataire.source = showlist[17]
            destinataire.identifiantSource = showlist[18]

            destinataire.adresseLivraison_nom = showlist[7]
            destinataire.adresseLivraison_numero = showlist[8]
            destinataire.adresseLivraison_rue = showlist[9]
            destinataire.adresseLivraison_complement_1 = showlist[10]
            destinataire.adresseLivraison_complement_2 = showlist[11]
            destinataire.adresseLivraison_codePostal = showlist[12]
            destinataire.adresseLivraison_localite = showlist[13]

            destinataire.fk_Pays = None
            destinataire.fk_TypeDestinataire = None

            pays = Pays_pour_Destinataire.objects.all()
            for items in pays:
                if items.nom == request.POST.get('pays'):
                    destinataire.fk_Pays = items
            typedest = TypeDestinataire_pour_Destinataire.objects.all()
            for items in typedest:
                if items.nom == request.POST.get('typedest'):
                    destinataire.fk_TypeDestinataire = items

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
            'settings' : menuimages.objects.all(),
            'id' :request.GET.get('id'),
            'umsortie' : UniteManutentionSortie.objects.all(),
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
            destinataire.departement = showlist[14]
            destinataire.adresseFacturation = showlist[15]
            destinataire.source = showlist[17]
            destinataire.identifiantSource = showlist[18]
            destinataire.adresseLivraison_nom = showlist[7]
            destinataire.adresseLivraison_numero = showlist[8]
            destinataire.adresseLivraison_rue = showlist[9]
            destinataire.adresseLivraison_complement_1 = showlist[10]
            destinataire.adresseLivraison_complement_2 = showlist[11]
            destinataire.adresseLivraison_codePostal = showlist[12]
            destinataire.adresseLivraison_localite = showlist[13]
            destinataire.idDestinataire = showlist[26]

            destinataire.fk_Pays = None
            destinataire.fk_TypeDestinataire = None

            pays = Pays_pour_Destinataire.objects.all()
            for items in pays:
                if items.nom == request.POST.get('pays'):
                    destinataire.fk_Pays = items
            typedest = TypeDestinataire_pour_Destinataire.objects.all()
            for items in typedest:
                if items.nom == request.POST.get('typedest'):
                    destinataire.fk_TypeDestinataire = items
                    return HttpResponse("It has been posted by lapost")
            destinataire.save()
            return HttpResponse("Error " + request.POST.get('typedest') + " "+ items.nom)

    def get(self, request):
        context = {
            'destype' :TypeDestinataire_pour_Destinataire.objects.all(),
            'des' :Destinataire.objects.all(),
            'pays':Pays_pour_Destinataire.objects.all(),
            'settings' : menuimages.objects.all(),
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
            'settings' : menuimages.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class colisadd(ListView):
    template_name = "colisadd.html"

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
            'settings' : menuimages.objects.all(),
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
            'settings' : menuimages.objects.all(),
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
            print("there -------------------------" + showlist[0])
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
                        request.POST.get('cont'), request.POST.get('commentaire'),]
            client = Client.objects.get(idClient=showlist[1])
            zne = TypeZoneDepot.objects.all()
            znedebug = False
            for zone in zne:
                if request.POST.get('zone') == zone.nom:
                    znedebug = True
                    client.fk_TypeZone = zone
                if showlist[7] == "":
                    client.fk_TypeZone = None
            tde = TypeDestinataire_pour_Destinataire.objects.all()
            tdedebug = False
            for typed in tde:
                if request.POST.get('typedest') == typed.nom:
                    tdedebug = True
                    client.fk_TypeDestinataire = typed
                if request.POST.get('typedest') == "":
                    client.fk_TypeDestinataire = None
            tfo = TypeFournisseur_pour_Fournisseur.objects.all()
            tfodebug = False
            for typefo in tfo:
                if request.POST.get('typefour') == typefo.nom:
                    tfodebug = True
                    client.fk_TypeFournisseur = typefo
                if request.POST.get('typefour') == "":
                    client.fk_TypeFournisseur = None
            tar = typeArticle_pour_Article.objects.all()
            tardebug = False
            for typea in tar:
                if request.POST.get('typeart') == typea.nom:
                    tardebug = True
                    client.fk_TypeArticle = typea
                if request.POST.get('typeart') == "":
                    client.fk_TypeArticle = None
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
            'typez' : TypeZoneDepot.objects.all(),
            'typed' : TypeDestinataire_pour_Destinataire.objects.all(),
            'typef' : TypeFournisseur_pour_Fournisseur.objects.all(),
            'typea' : typeArticle_pour_Article.objects.all(),
            'bcs' : BonCommandeSortie.objects.all(),
            'bce' : BonCommandeEntree.objects.all(),
            'entree' : BonLivraisonEntree.objects.all(),
            'settings' : menuimages.objects.all(),
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
            client.fk_TypeArticle = None
            client.fk_TypeDestinataire = None
            client.fk_TypeFournisseur = None
            client.fk_TypeZone = None
            for items in cli:
                if items.idClient == request.POST.get('id'):
                    return HttpResponse("Client aldready registered")

            zne = TypeZoneDepot.objects.all()
            znedebug = False
            for zone in zne:
                if request.POST.get('zone') == zone.nom:
                    znedebug = True
                    client.fk_TypeZone = zone
            tde = TypeDestinataire_pour_Destinataire.objects.all()
            tdedebug = False
            for typed in tde:
                if request.POST.get('typedest') == typed.nom:
                    tdedebug = True
                    client.fk_TypeDestinataire = typed
            tfo = TypeFournisseur_pour_Fournisseur.objects.all()
            tfodebug = False
            for typefo in tfo:
                if request.POST.get('typefour') == typefo.nom:
                    tfodebug = True
                client.fk_TypeFournisseur = typefo
            tar = typeArticle_pour_Article.objects.all()
            tardebug = False
            for typea in tar:
                if request.POST.get('typeart') == typea.nom:
                    tardebug = True
                    client.fk_TypeArticle = typea
            if tfodebug is False:
                return HttpResponse(" Error you choosed a broken fk1")
            #if znedebug is False:
            #return HttpResponse(" Error you choosed a broken fk2")
            if tdedebug is False:
                return HttpResponse(" Error you choosed a broken fk3")
            if tardebug is False:
                return HttpResponse(" Error you choosed a broken fk4")
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
                zne = TypeZoneDepot.objects.all()
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
            'typez' : TypeZoneDepot.objects.all(),
            'typed' : TypeDestinataire_pour_Destinataire.objects.all(),
            'typef' : TypeFournisseur_pour_Fournisseur.objects.all(),
            'typea' : typeArticle_pour_Article.objects.all(),
            'bcs' : BonCommandeSortie.objects.all(),
            'bce' : BonCommandeEntree.objects.all(),
            'rlc' : RoleContact_pour_Client.objects.all(),
            'con' : Contact_pour_Client.objects.all(),
            'settings' : menuimages.objects.all(),
            'activate' : 'on',
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#unitemanutention

class umereference(ListView):
    template_name = "unitemanutentionentreereference.html"

    def get(self, request):
        context = {
            'activate' : 'on',
            'ume' : UniteManutentionEntree.objects.all(),
            'col' : Colis.objects.all(),
            'art' : Article.objects.all(),
            'bcs' : BonCommandeSortie.objects.all(),
            'lbcs' : LigneBonCommandeSortie_pour_BonCommandeSortie.objects.all(),
            'name' : request.GET.get('name'),
            'settings' : menuimages.objects.all(),
        }
        return render(request, self.template_name, context)

class ume(ListView):
    template_name = "unitemanutentionentree.html"

    def delete(request):
        if request.method == 'POST':
            ume = UniteManutentionEntree.objects.all()
            for items in ume:
                if items.idUniteManutentionEntree == request.POST.get('id'):
                    data = UniteManutentionEntree.objects.get(idUniteManutentionEntree=request.POST['id'])
                    data.delete()
                    return HttpResponse("road to delete.")
            return HttpResponse("Error on delete.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'ume' : UniteManutentionEntree.objects.all(),
            'settings' : menuimages.objects.all(),
        }
        return render(request, self.template_name, context)

class umeadd(ListView):
    template_name = "unitemanutentionentreeadd.html"

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('uminc'),
                        request.POST.get('numum'), request.POST.get('dater'),
                        request.POST.get('colisaff'), request.POST.get('prodaff'),]

            umentree = UniteManutentionEntree.objects.all()
            ume = UniteManutentionEntree()
            ume.idUniteManutentionEntree = showlist[0]

            ume.stock = showlist[1]
            ume.numero = showlist[2]
            ume.afficherQuantiteColis = showlist[4]
            ume.afficherQuantiteProduits = showlist[5]
            ume.dateReception = showlist[3]
            ume.fk_BonLivraisonEntree = None
            ume.fk_ZoneDepot = None
            ume.c_nom = ""
            ume.c_nomCompte = ""
            ume.c_horodatage = ""
            ume.m_nom = ""
            ume.m_nomCompte = ""
            ume.m_horodatage = ""

            id = 0
            try:
                go = UniteManutentionEntree.objects.get(idUniteManutentionEntree=showlist[0])
                for myume in umentree:
                    if id < int(myume.idUniteManutentionEntree):
                        id = int(myume.idUniteManutentionEntree)
                id+=1
                ume.idUniteManutentionEntree = str(id) #je gère que cet id est déjà prit
            except UniteManutentionEntree.DoesNotExist:
                '''ici je fais rien car il n'y a pas d'"ume" avec un id déjà pris, donc je peux laisser le lve se faire save ;)'''
            ume.save()
            if id == 0:
                return HttpResponse(showlist[0]) #retours pour signifier un succès
            else:
                return HttpResponse(str(id)) #retours pour signifier un succès
            #return HttpResponse("road to create ume.")
        return HttpResponse("Error on delete.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'ume' : UniteManutentionEntree.objects.all(),
        }
        return render(request, self.template_name, context)

class umemodify(ListView):
    template_name = "unitemanutentionentreemodify.html"

    def delete_colis(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'),]
            colis = Colis.objects.get(id=showlist[0])
            colis.delete()
            return HttpResponse("colis removed.")
        return HttpResponse("Error.")

    def printer(request): #mets la valeur imprime a 1 pour géré si on peut coller ou pas l'etiquette
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            colis = Colis.objects.get(idColis=showlist[0])
            colis.imprime = "1"
            colis.save()
            return HttpResponse("colis removed.")
        return HttpResponse("Error.")

    def delieums(request): #on va chercher le colis dans l'unite de manutention sortie pui dans la ligne bon commande sortie pour lui "enliever" la qte et le colis, puis son fk unitemanutentionsortie est a None
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            colis = Colis.objects.get(idColis=showlist[0])
            ums = UniteManutentionSortie.objects.all()
            bcs = BonCommandeSortie.objects.all()
            lbcs = LigneBonCommandeSortie_pour_BonCommandeSortie.objects.all()
            for myums in ums:
                if colis.fk_UniteManutentionSortie:
                    if colis.fk_UniteManutentionSortie.idUniteManutentionSortie == myums.idUniteManutentionSortie:
                        for mybcs in bcs:
                            if myums.fk_BonCommandeSortie.idBonCommandeSortie == mybcs.idBonCommandeSortie:
                                for mylbcs in lbcs:
                                    if mylbcs.fk_BonCommandeSortie.idBonCommandeSortie == mybcs.idBonCommandeSortie:
                                        if mylbcs.fk_Article == colis.fk_Article:
                                            print("found !!!!!!!!!!! at the line of bon de commande sortie " + str(mylbcs))
                                            mylbcs.quantiteProduitLivre = str(int(mylbcs.quantiteProduitLivre) - int(colis.quantiteProduit))
                                            mylbcs.quantiteColisLivre = str(int(mylbcs.quantiteColisLivre) - 1)
                                            mylbcs.quantiteProduitCommandestats = str(int(mylbcs.quantiteProduitCommandestats) + int(colis.quantiteProduit))
                                            colis.fk_UniteManutentionSortie = None
                                            mylbcs.save()
                                            colis.save()
            return HttpResponse("colis removed out of this UMs.")
        return HttpResponse("Error.")

    def modify(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('uminc'),
                        request.POST.get('numum'), request.POST.get('dater'),
                        request.POST.get('colisaff'), request.POST.get('prodaff'),
                        request.POST.get('zonedep'), request.POST.get('ble')]
            try:
                ume = UniteManutentionEntree.objects.get(idUniteManutentionEntree=showlist[0])
                ume.stock = showlist[1]
                ume.numero = showlist[2]
                ume.afficherQuantiteColis = showlist[4]
                ume.afficherQuantiteProduits = showlist[5]
                ume.dateReception = showlist[3]
                try:
                    zonedp = ZoneDepot_pour_TypeZoneDepot.objects.get(nom=showlist[6]) #on change la zone de dépots du BL entree donc "ou" va être la palette
                    ume.fk_ZoneDepot = zonedp
                    print("zone ok gg!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                except Exception as e:
                    print("error1 -- " + str(e))
            except UniteManutentionEntree.DoesNotExist:
                print ("error3")
                return HttpResponse("Error ume Not found.")
            ume.save()
            return HttpResponse("road to create ume.")
        return HttpResponse("Error.")

    def createligne(request): #utiliser pour la modication pour gagner du temps car on utilise "get" si l'object existe ou alors on le crée
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('ncolis'),
                        request.POST.get('codef'), request.POST.get('designation'),
                        request.POST.get('nlot'), request.POST.get('datep'),
                        request.POST.get('qtecolis'), request.POST.get('numerote'),
                        request.POST.get('confirme'), request.POST.get('retourncolis'),
                        request.POST.get('colle'), request.POST.get('litige'),
                        request.POST.get('decilitige')]
            existcoli = 0
            try:
                mycolis = Colis.objects.get(idColis=showlist[1])
                existcoli = 1
                print("Before - " + str(mycolis.fk_UniteManutentionEntree.idUniteManutentionEntree) + " AFTER - " + str(showlist[0]))
                if mycolis.fk_UniteManutentionEntree.idUniteManutentionEntree != showlist[0]:
                    existcoli = 2
                    print("COLIS NOT IN THIS UME SO I DO A NEW ONE")
                    mycolis = Colis()
                    mycolis.fk_UniteManutentionSortie = None
            except Colis.DoesNotExist:
                mycolis = Colis()
                mycolis.fk_UniteManutentionSortie = None
            mycolis.idColis = showlist[1]
            #mycolis.fk_ZoneDepot = UniteManutentionEntree.objects.get(idUniteManutentionEntree=showlist[0]).fk_BonLivraisonEntree.fk_ZoneDepot_pour_TypeZoneDepot
            mycolis.fk_ZoneDepot = None
            mycolis.numeroLot = showlist[4]
            mycolis.datePeremption = showlist[5]
            mycolis.quantiteProduit = showlist[6]
            mycolis.numerotation = showlist[7]
            mycolis.emplacementConfirme = showlist[8]
            #mycolis. = showlist[9]
            mycolis.colle = showlist[10]

            allcol = Colis.objects.all()
            alitige = Litige.objects.all()
            dlitige = LitigeDecision.objects.all()
            carticle = Article.objects.all()

            mycolis.fk_Article = None
            for items in carticle:
                if items.designationClient == showlist[3]:
                    mycolis.fk_Article = Article.objects.get(designationClient=showlist[3])

            mycolis.fk_litige = None
            for items in alitige:
                if items.nom == showlist[11]:
                    print ("GG FGOZE9PUAZ9EU F9PUAZ9")
                    mycolis.fk_litige = Litige.objects.get(nom=showlist[11])

            mycolis.fk_LitigeDecision = None
            for items in dlitige:
                if items.nom == showlist[12]:
                    mycolis.fk_LitigeDecision = LitigeDecision.objects.get(nom=showlist[12])

            '''print ("id == " + showlist[0])
            print ("ncol == " + str(showlist[1]))
            print ("codef == " + str(showlist[2]))
            print ("desig == " + str(showlist[3]))
            print ("ncol == " + str(showlist[4]))
            print ("datep == " + str(showlist[5]))
            print ("qtec == " + str(showlist[6]))
            print ("nume == " + str(showlist[7]))
            print ("conf == " + str(showlist[8]))
            print ("retnc == " + str(showlist[9]))
            print ("colle == " + str(showlist[10]))
            '''
            print ("litige == " + str(showlist[11]))
            print ("decilitige == " + str(showlist[12]))

            id = 0
            if existcoli == 0:
                try:
                    go = Colis.objects.get(idColis=showlist[1])
                    for colis in allcol:
                        if id < int(colis.idColis):
                            id += int(colis.idColis)
                    id+=1
                    mycolis.idColis = str(id) #je gère que cet id est déjà prit
                except Colis.DoesNotExist:
                    '''ici je fais rien car il n'y a pas d'"ume" avec un id déjà pris, donc je peux laisser le lve se faire save ;)'''

            if existcoli == 2:
                try:
                    go = Colis.objects.get(idColis=showlist[1])
                    for colis in allcol:
                        if id < int(colis.idColis):
                            id += int(colis.idColis)
                    id+=1
                    mycolis.idColis = str(id) #je gère que cet id est déjà prit
                except Colis.DoesNotExist:
                    '''ici je fais rien car il n'y a pas d'"ume" avec un id déjà pris, donc je peux laisser le lve se faire save ;)'''

            mycolis.fk_UniteManutentionEntree = UniteManutentionEntree.objects.get(idUniteManutentionEntree=showlist[0])
            mycolis.save()
            mycolis.idColis = str(mycolis.id)
            mycolis.save()
            if id == 0:
                return HttpResponse(showlist[0]) #retours pour signifier un succès
            else:
                return HttpResponse(str(id)) #retours pour signifier un succès
            #return HttpResponse("road to create ume.")
        return HttpResponse("Error not a post.")

    def get(self, request):
        context = {
            'article' : Article.objects.all(),
            'litige' : Litige.objects.all(),
            'decilitige' : LitigeDecision.objects.all(),
            'settings' : menuimages.objects.all(),
            'colis' : Colis.objects.all(),
            'ume' : UniteManutentionEntree.objects.all(),
            'zdt' : ZoneDepot_pour_TypeZoneDepot.objects.all(),
            'id' :request.GET.get('id'),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class setting(UpdateView):
    '''template_name = "setting.html"
    #success_url = reverse_lazy('')
    form_class = PostForm
    initial = {'key': 'value'}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = imgaccueil()
            obj.title = form['title']
            obj.cover = form['cover']
            obj.save()
            return HttpResponse("good input.")
        return HttpResponse("bad input.")

    def get(self, request):
        #success_url = reverse_lazy('')
        form = self.form_class(initial=self.initial)
        context = {
            'activate' : 'on',
            'object_list': imgaccueil.objects.all(),
            'form': form,
        }
        return render(request, self.template_name, context) #request permet de savoir si je suis connecté'''

    model = menuimages.objects.filter(pk=1)
    form_class = PostForm
    secondform_class = UserCreationForm
    template_name = 'setting.html'
    success_url = reverse_lazy('setting')
    #return HttpResponse("No access there")

    def get_context_data(self, **kwargs):
        context = super(setting, self).get_context_data(**kwargs)
        context['settings'] = menuimages.objects.all()
        context['userform'] = self.secondform_class(self.request.GET)
        return context

    def reset(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'),]
            img = menuimages.objects.get(pk=1)
            img.cover1.delete(save=True)
            img.cover2.delete(save=True)
            img.cover3.delete(save=True)
            img.cover4.delete(save=True)
            img.cover5.delete(save=True)
            img.cover6.delete(save=True)
            img.cover7.delete(save=True)
            img.cover8.delete(save=True)
            img.cover9.delete(save=True)
            img.cover10.delete(save=True)
            img.cover11.delete(save=True)
            img.cover12.delete(save=True)
            img.cover13.delete(save=True)
            #img.save()
            return HttpResponse("road to create ume.")
        return HttpResponse("Error on delete.")

    def get_queryset(self):
        queryset = menuimages.objects.filter(pk=1)
        return queryset
    def get_success_url(self):
        return reverse('setting', kwargs={'pk': 1})
        #return reverse('index')

    '''def register(request):
        if request.method == 'POST':
            form = UserCreationForm(Request.POST)
            if form.is_valid():
                form.save()
                return redirect('/account')
            else:
                form = UserCreationForm()

                args = {'regiform': form}
                return render{request, 'registration/register.html', args}'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class register(CreateView):
    template_name = "registration/register.html"

    def get(self, request):
        model = User
        form_class = UserCreationForm
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'ume' : UniteManutentionEntree.objects.all(),
            'userform' : form_class(self.request.GET),
            'users' : User.objects.all(),
        }
        return render(request, self.template_name, context)

def recregister(request):
    if request.POST:
        form_class = UserCreationForm(request.POST)
        if form_class.is_valid():
            form_class.save()
            return redirect('/register')
        form_class = UserCreationForm()
        context = {
            'userform' : form_class,
        }
        return render(request, "registration/register.html", context)
    return HttpResponse("403: No access granted")

def deleteuser(request):
    if request.POST:
        showlist = [request.POST.get('id'),]
        u = User.objects.get(pk=showlist[0])
        u.delete()
        print(str(showlist[0]))
        return HttpResponse("success")
    return HttpResponse("403: No access granted")

class create_typef(ListView):
    template_name = "create_type_fournisseur.html"

    def delete(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            data = TypeFournisseur_pour_Fournisseur.objects.get(idTypeFournisseur=showlist[0])
            data.delete()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'typef' : TypeFournisseur_pour_Fournisseur.objects.all(),
        }
        return render(request, self.template_name, context)

class create_typef_add(ListView):
    template_name = "create_type_fournisseuradd.html"

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'typef' : TypeFournisseur_pour_Fournisseur.objects.all(),
        }
        return render(request, self.template_name, context)

    def saveit(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'),
                        request.POST.get('name')]
            typef = TypeFournisseur_pour_Fournisseur()
            typef.idTypeFournisseur = showlist[0]
            typef.nom = showlist[1]
            typef.save()
        return HttpResponse("Error ZONE RESTRICTED.")

class modif_typef(ListView):
    template_name = "modif_type_fournisseur.html"

    def get(self, request):
        context = {
            'activate' : 'on',
            'id' :request.GET.get('id'),
            'settings' : menuimages.objects.all(),
            'typef' : TypeFournisseur_pour_Fournisseur.objects.all(),
        }
        return render(request, self.template_name, context)

class zonesdepot(ListView):
    template_name = "Zone_depot.html"

    def delete(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            data = ZoneDepot_pour_TypeZoneDepot.objects.get(idZoneDepot=showlist[0])
            data.delete()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def createnewzone(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('client'), request.POST.get('name'),]
            data = ZoneDepot_pour_TypeZoneDepot()
            if (showlist[1] != '---'):
                cli = Client.objects.get(idClient=showlist[1])
            else:
                cli = None
            data.nom = showlist[2]
            data.idZoneDepot = showlist[0]
            if (cli != None):
                data.fk_Client = cli
            else:
                data.fk_Client = None
            #print("id == " + showlist[0] + "cli == " + cli.nom + "name == " + showlist[2])
            data.save()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'zoned' : ZoneDepot_pour_TypeZoneDepot.objects.all(),
            'cli' : Client.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)

class typedest(ListView):
    template_name = "typedestinataire.html"

    def delete(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            data = TypeDestinataire_pour_Destinataire.objects.get(idTypeDestinataire=showlist[0])
            data.delete()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('name'),]
            try:
                data = TypeDestinataire_pour_Destinataire.objects.get(idTypeDestinataire =showlist[0])
                print("found")
            except TypeDestinataire_pour_Destinataire.DoesNotExist:
                print("create")
                data = TypeDestinataire_pour_Destinataire()
                data.idTypeDestinataire = showlist[0]
            data.nom = showlist[1]
            data.save()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'typed' : TypeDestinataire_pour_Destinataire.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)

class typeart(ListView):
    template_name = "typearticle.html"

    def delete(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            data = typeArticle_pour_Article.objects.get(idTypeArticle=showlist[0])
            data.delete()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('name'),]
            try:
                data = typeArticle_pour_Article.objects.get(idTypeArticle=showlist[0])
                print("found")
            except typeArticle_pour_Article.DoesNotExist:
                print("create")
                data = typeArticle_pour_Article()
                data.idTypeArticle = showlist[0]
            data.nom = showlist[1]
            data.save()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'typea' : typeArticle_pour_Article.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)

#gestion des zones pour clients
class typezone(ListView):
    template_name = "typezonedepot.html"

    def delete(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            data = TypeZoneDepot.objects.get(idTypeZoneDepot=showlist[0])
            data.delete()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('name'),]
            try:
                data = TypeZoneDepot.objects.get(idTypeZoneDepot=showlist[0])
                print("found")
            except TypeZoneDepot.DoesNotExist:
                print("create")
                data = TypeZoneDepot()
                data.idTypeZoneDepot = showlist[0]
            data.nom = showlist[1]
            data.save()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'typez' : TypeZoneDepot.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)

#gestion des roles contactes
class typecont(ListView):
    template_name = "typecontact.html"

    def delete(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            data = RoleContact_pour_Client.objects.get(idRoleContact=showlist[0])
            data.delete()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('name'),]
            try:
                data = RoleContact_pour_Client.objects.get(idRoleContact=showlist[0])
                print("found")
            except RoleContact_pour_Client.DoesNotExist:
                print("create")
                data = RoleContact_pour_Client()
                data.idRoleContact = showlist[0]
            data.nom = showlist[1]
            data.save()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'rlc' : RoleContact_pour_Client.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)

#gestion des pays pour destinataire
class pays(ListView):
    template_name = "pays.html"

    def delete(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id')]
            data = Pays_pour_Destinataire.objects.get(idPays=showlist[0])
            data.delete()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('name'),]
            try:
                data = Pays_pour_Destinataire.objects.get(idPays=showlist[0])
                print("found")
            except Pays_pour_Destinataire.DoesNotExist:
                print("create")
                data = Pays_pour_Destinataire()
                data.idPays = showlist[0]
            data.nom = showlist[1]
            data.save()
            return HttpResponse("create successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'pays' : Pays_pour_Destinataire.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)

#gestion des litiges
class litiges(ListView):
    template_name = "litiges.html"

    def deletelitige(request):
        if request.method == 'POST':
            showlist = [request.POST.get('nom')]
            data = Litige.objects.get(nom=showlist[0])
            data.delete()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def deletedecilitige(request):
        if request.method == 'POST':
            showlist = [request.POST.get('nom')]
            data = LitigeDecision.objects.get(nom=showlist[0])
            data.delete()
            return HttpResponse("delete successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'litige' : Litige.objects.all(),
            'decilitige' : LitigeDecision.objects.all(),
            'id' :request.GET.get('id'),
        }
        return render(request, self.template_name, context)

class litigesadd(ListView):
    template_name = "litigesadd.html"

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('name'),request.POST.get('id')]
            data = Litige()
            data.nom = showlist[0]
            data.idLitige = showlist[1]
            data.save()
            return HttpResponse("added successfully.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'litige' : Litige.objects.all(),
            'id' :request.GET.get('id'),
        }
        return render(request, self.template_name, context)

class decilitigesadd(ListView):
    template_name = "decilitigesadd.html"

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('name'),request.POST.get('id')]
            data = LitigeDecision()
            data.nom = showlist[0]
            data.idLitige = showlist[1]
            data.save()
            return HttpResponse("added successfully.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'decilitige' : LitigeDecision.objects.all(),
            'id' :request.GET.get('id'),
        }
        return render(request, self.template_name, context)

class litigesmodify(ListView):
    template_name = "litigesmodify.html"

    def modify(request):
        if request.method == 'POST':
            showlist = [request.POST.get('name'),request.POST.get('id')]
            data = Litige.objects.get(idLitige=showlist[1])
            data.nom = showlist[0]
            data.save()
            return HttpResponse("change successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'litige' : Litige.objects.all(),
            'id' :request.GET.get('id'),
        }
        return render(request, self.template_name, context)

class decilitigesmodify(ListView):
    template_name = "decilitigesmodify.html"

    def modify(request):
        if request.method == 'POST':
            showlist = [request.POST.get('name'),request.POST.get('id')]
            data = LitigeDecision.objects.get(idLitige=showlist[1])
            data.nom = showlist[0]
            data.save()
            return HttpResponse("change successfull.")
        return HttpResponse("Error ZONE RESTRICTED.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'decilitige' : LitigeDecision.objects.all(),
            'id' :request.GET.get('id'),
        }
        return render(request, self.template_name, context)

        #fin des réglages dans settings
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class ums(ListView):
    template_name = "unitemanutentionsortie.html"

    def delete(request):
        if request.method == 'POST':
            ums = UniteManutentionSortie.objects.all()
            for items in ums:
                if items.idUniteManutentionSortie == request.POST.get('id'):
                    data = UniteManutentionSortie.objects.get(idUniteManutentionSortie=request.POST['id'])
                    data.delete()
                    return HttpResponse("road to delete.")
            return HttpResponse("Error on delete.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'ums' : UniteManutentionSortie.objects.all(),
            'col' : Colis.objects.all(),

            'article' : Article.objects.all(),
            'litige' : Litige.objects.all(),
            'decilitige' : LitigeDecision.objects.all(),

            'settings' : menuimages.objects.all(),
        }
        return render(request, self.template_name, context)

class umsadd(ListView): #pas utilisé car les um sont crée via un script (uploadbc)
    template_name = "unitemanutentionsortieadd.html"

    def create(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'),]
            umsortie = UniteManutentionSortie.objects.all()
            ums = UniteManutentionSortie()
            ums.idUniteManutentionSortie = showlist[0]
            ums.fk_BonLivraisonSortie = None
            ums.fk_ZoneDepot = None
            ums.c_nom = ""
            ums.c_nomCompte = ""
            ums.c_horodatage = ""
            ums.m_nom = ""
            ums.m_nomCompte = ""
            ums.m_horodatage = ""
            ums.numero = ""
            ums.dateReception = ""
            ums.stock = ""
            ums.save()
            return HttpResponse("road to create ume.")
        return HttpResponse("Error on delete.")

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'ums' : UniteManutentionSortie.objects.all(),
        }
        return render(request, self.template_name, context)

class umsmodify(ListView):
    template_name = "unitemanutentionsortiemodify.html"

    def delete_colis(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'),]
            colis = Colis.objects.get(idColis=showlist[0])
            colis.delete()
            return HttpResponse("colis removed.")
        return HttpResponse("Error.")

    def modify(request):
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('litige'),
                        request.POST.get('decilitige')]
            umsortie = UniteManutentionSortie.objects.all()
            ums = UniteManutentionSortie()
            return HttpResponse("road to create ume.")
        return HttpResponse("Error.")

    def createligne(request): #pas utilisé
        if request.method == 'POST':
            showlist = [request.POST.get('id'), request.POST.get('ncolis'),
                        request.POST.get('codef'), request.POST.get('designation'),
                        request.POST.get('nlot'), request.POST.get('datep'),
                        request.POST.get('qtecolis'), request.POST.get('numerote'),
                        request.POST.get('confirme'), request.POST.get('retourncolis'),
                        request.POST.get('colle'), request.POST.get('litige'),
                        request.POST.get('decilitige')]
            try:
                mycolis = Colis.objects.get(idColis=showlist[1])
            except Colis.DoesNotExist:
                mycolis = Colis()
            mycolis.fk_UniteManutentionSortie = showlist[1]
            #mycolis.fk_UniteManutentionEntree = UniteManutentionEntree.objects.get(idUniteManutentionEntree=showlist[0])
            mycolis.idColis = showlist[1]
            #mycolis.fk_ZoneDepot = UniteManutentionEntree.objects.get(idUniteManutentionEntree=showlist[0]).fk_ZoneDepot
            mycolis.numeroLot = showlist[4]
            mycolis.datePeremption = showlist[5]
            mycolis.quantiteProduit = showlist[6]
            mycolis.numerotation = showlist[7]
            mycolis.emplacementConfirme = showlist[8]
            #mycolis. = showlist[9]
            mycolis.colle = showlist[10]

            alitige = Litige.objects.all()
            dlitige = LitigeDecision.objects.all()
            carticle = Article.objects.all()

            mycolis.fk_Article = None
            for items in carticle:
                if items.designationClient == showlist[3]:
                    mycolis.fk_Article = Article.objects.get(designationClient=showlist[3])

            mycolis.fk_litige = None
            for items in alitige:
                if items.nom == showlist[11]:
                    print ("Found")
                    mycolis.fk_litige = Litige.objects.get(nom=showlist[11])

            mycolis.fk_LitigeDecision = None
            for items in dlitige:
                if items.nom == showlist[12]:
                    mycolis.fk_LitigeDecision = LitigeDecision.objects.get(nom=showlist[12])
            print ("litige == " + str(showlist[11]))
            print ("decilitige == " + str(showlist[12]))
            #mycolis.save()
            return HttpResponse("road to create ume.")
        return HttpResponse("Error.")

    def dateouverture(request):
        if request.method == 'POST':
            print(request.POST.get('dateouverture'))
        try:
            ums = UniteManutentionSortie.objects.get(idUniteManutentionSortie=request.POST.get('id'))
            ums.dateOuverture = request.POST.get('dateouverture')
            ums.save()
        except menuimages.DoesNotExist:
            ums = None
            return HttpResponse("good.")
        return HttpResponse("Error.")

    def datefermeture(request):
        if request.method == 'POST':
            print(request.POST.get('datefermeture'))
        try:
            ums = UniteManutentionSortie.objects.get(idUniteManutentionSortie=request.POST.get('id'))
            ums.dateFermeture = request.POST.get('datefermeture')
            ums.save()
        except menuimages.DoesNotExist:
            ums = None
            return HttpResponse("good.")
        return HttpResponse("Error.")

    def dateexpedition(request):
        if request.method == 'POST':
            print(request.POST.get('dateexpedition'))
        try:
            ums = UniteManutentionSortie.objects.get(idUniteManutentionSortie=request.POST.get('id'))
            ums.dateExpedition = request.POST.get('dateexpedition')
            ums.save()
        except menuimages.DoesNotExist:
            ums = None
            return HttpResponse("good.")
        return HttpResponse("Error.")

    def get(self, request):
        context = {
            'article' : Article.objects.all(),
            'litige' : Litige.objects.all(),
            'decilitige' : LitigeDecision.objects.all(),
            'settings' : menuimages.objects.all(),
            'colis' : Colis.objects.all(),
            'ums' : UniteManutentionSortie.objects.all(),
            'id' :request.GET.get('id'),
            'activate' : 'on'
        }
        return render(request, self.template_name, context)

#etiquette Um (impression) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class etiquetteume(ListView):
    template_name = "etiquetteume.html"

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'col' : Colis.objects.all(),
            'ume' : UniteManutentionEntree.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)

class etiquetteumecolis(ListView):
    template_name = "etiquetteumecolis.html"

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'col' : Colis.objects.all(),
            'ume' : UniteManutentionEntree.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)

class etiquetteums(ListView):
    template_name = "etiquetteums.html"

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'ums' : UniteManutentionSortie.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)

class etiquetteumscolissage(ListView):
    template_name = "etiquetteumscolissage.html"

    def get(self, request):
        context = {
            'activate' : 'on',
            'settings' : menuimages.objects.all(),
            'ums' : UniteManutentionSortie.objects.all(),
            'colis' : Colis.objects.all(),
            'id' :request.GET.get('id'),
            'vuegen' :request.GET.get('vuegen'),
            'creation' :request.GET.get('creation'),
        }
        return render(request, self.template_name, context)
