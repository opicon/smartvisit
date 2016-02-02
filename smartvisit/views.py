# -*- coding: utf-8 -*-

"""
Created on Sat Jan  2 00:42:25 2016

@author: Théo
"""


from django.shortcuts import render
#from django.http import HttpResponse
#import datetime #librairie pour récupérer le moment de la requête

# Create your views here.
#==============================================================================
from smartvisit.models import Places
def home(request):
    ''' vue de la page d'accueil du module avec la page d'accueil '''
    return render(request, 'smartvisit/home.html',locals())
 
#==============================================================================
from smartvisit.forms import request_user_form #on récupère le formulaire de demande de trajet utilisateur
import smartvisit.algos_gmaps as algos #on récupère les algos d'extraction, de traitement et d'optimisation des données

def request_user(request):
    ''' vue de la page de requête de l'utilisateur pour une visite'''
    
    if request.method == 'POST':  #S'il s'agit d'une requête POST
        form = request_user_form(request.POST)  #on récupère les données du formulaires de requête de l'utilisateur
        
        if form.is_valid(): #Si les données rentrées par l'utilisateur sont conformes

            #On récupère les données du formulaire
            startpoint = form.cleaned_data['startpoint']
            endpoint = form.cleaned_data['endpoint']
            mode = form.cleaned_data['mode']
            duree = algos.hms_to_s(form.cleaned_data['heures'],form.cleaned_data['minutes'])
            categories = form.cleaned_data['category']

            #On récupère les waypoints potentiels dans la base de données correspondant aux catégories sélectionnées par l'utilisateur
            waypoints = []
            for category in categories:
                for place in Places.objects.filter(categorie=category):                         
                    waypoints += [{'id':place.id,                                               #on stocke l'id du point de passage dans la base de donnée pour récupérer l'ensemble des données plus tard
                                   'location': {'lat':place.latitude,'lng':place.longitude},    #les coordonnées pour l'algorithme
                                   'rating':place.score,                                         #son score pour l'algorithme
                                   'categorie':place.categorie}]                                #la catégorie pour l'affichage

            #On trouve le trajet optimisé passant par le maximum de points avec l'algorithme           
            algo = algos.optimization_algo_1(startpoint, endpoint, mode, duree, waypoints = waypoints)

            #on récupère les paramètres de l'itinéraire final
            parameters = algo[0]
            
            #Et l'ensemble des données utiles pour l'affichage qui sortent de l'algorithme        
            message = algo[2]                   #Le message potentiel à afficher
            bounds = algo[3]                    #Les bornes de l'itinéraire choisi pour l'affichage de la carte
            boundsNE = bounds['northeast']      
            boundsSW = bounds['southwest']
            
            #Récupération des autres paramètres dans le dictionnaire 'parameters'  
            waypoints_id = [x['id'] for x in parameters['waypoints']]   #ids des points de passage finaux sélectionnés
            waypoints_coord = []                                      #on récupère les coordonnées pour l'affichage des marqueurs
            waypoints_display = []                                    #données pour l'affichage
            
            #Pour chaque id sélectionnée par l'algorithme on récupère les données intéressantes dans la base de données
            k = 0                                      #ensemble des données que l'on récupère à partir des ids pour afficher les résultats
            for waypoint_id in waypoints_id:
                k += 1
                waypoint = Places.objects.filter(id=waypoint_id)[0]     #on récupère l'ensemble des données correspondants aux id finaux
                waypoints_coord += [{'lat':waypoint.latitude,'lng':waypoint.longitude}]
                waypoints_display += [[waypoint.id,waypoint.adresse,waypoint.ville,waypoint.categorie,waypoint.description,waypoint.wikipedia,waypoint.photo,k]]                #on peut insérer ici de ne pas seulement afficher le nom mais la catégorie, et une image par exemple
            
            #Autres paramètres à récupérer
            duration_request = algos.duration(parameters)               #durée totale de l'itinéraire proposé (affiché directemement en texte)
            distance_request = algos.distance(parameters)               #distance totale de l'itinéraire proposé (affiché directement en texte)
            
            #Récupération des coordonnées géographiques de tous les points            
            geo_sp = parameters['startpoint']['location']                   
            geo_ep = parameters['endpoint']['location']
            path_request = parameters['overview_polyline']              #Polyline permettant l'affichage du chemin
            possible = (algos.duration_value(parameters) < duree)       #Si l'itinéraire est faisable dans le temps imparti, cette variable booléenne est vraie
            envoi = True                                                #Requête bien envoyée

    else: #Si le formulaire n'est pas posté (POST), c'est que la requête est encore GET
        form = request_user_form()                                      #on crée donc un formulaire vide sur la page

    #Ensemble des lieux qui seront affichés
    all_places = Places.objects.all()
    all_waypoints = [{'location':{'lat':place.latitude,'lng':place.longitude},'categorie':place.categorie,'id':place.id,'name':place.adresse} for place in all_places]
    waypoints_monument = [x for x in all_waypoints if x['categorie'] == 'monument']
    waypoints_nature = [x for x in all_waypoints if x['categorie'] == 'nature']
    waypoints_art = [x for x in all_waypoints if x['categorie'] == 'art']
    waypoints_quartier = [x for x in all_waypoints if x['categorie'] == 'quartier']
    waypoints_insolite = [x for x in all_waypoints if x['categorie'] == 'insolite']
    waypoints_restaurant = [x for x in all_waypoints if x['categorie'] == 'restaurant']

    return render(request, 'smartvisit/request.html',locals()) #On renvoie la page html correspondante avec l'ensemble des variables locales
  

#==============================================================================  
from django.shortcuts import redirect
from smartvisit.forms import new_place_form  #Formulaire pour l'ajout de nouveau lieu

def post(request):
    '''Vue qui contrôle la page post permettant d'ajouter de nouveaux lieux'''

    if request.method == 'POST':  #S'il s'agit d'une requête POST
        form = new_place_form(request.POST)  #on récupère les données de formulaire
        if form.is_valid(): #Si elles sont bien valides

            new_place = form.save(commit=False) #on récupère les données de formulaire comme une nouvelle entrée dans la base de données
            new_place_name = new_place.adresse + ', ' + new_place.ville #on fusionne le nom et la ville pour former l'adresse
            new_place_coord = algos.coords(new_place_name)              #on recherche les coordonnées en fonction de l'adresse sur google maps
            new_place.latitude = new_place_coord[0]                     #récupération de la latitude
            new_place.longitude = new_place_coord[1]                    #récupération de la longitude
            new_place.score = 0                                         #score initialement nul
            new_place.save()                                            #on sauvegarde l'entrée dans la base de donnée
            
            envoi = True                                                #nouveau lieu bien envoyé
            return redirect(request_user)                                     #on redirige vers la page contenant tous les lieux

    else: #Si le formulaire n'est pas posté (POST), c'est que la requête est encore GET
        form = new_place_form()  #on crée donc un formulaire vide sur la page
    return render(request, 'smartvisit/post.html',locals())



