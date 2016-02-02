# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 19:26:50 2016

@author: Théo
"""
# Ensemble des algorithmes 
# - google maps (extraction API)
# - optimisation du chemin


#---------------------------------------------------------------------
# LIBRAIRIES

from datetime import datetime #pour utiliser le moment actuel dans l'extraction du chemin google maps 
from math import floor #arrondi inférieur


#---------------------------------------------------------------------
# AUTHENTIFICATION

Authentification_Key = 'AIzaSyAzjp6H9ZHtmUjf7b0mlgkGOrjD7sktFHQ' #clé d'authentification à l'API google maps

import googlemaps #importe la librairie d'extraction à l'API google maps
gmaps = googlemaps.Client(key = Authentification_Key) #crée un objet googlemaps accessible avec la clé qui permet de faire les requêtes à l'API

#---------------------------------------------------------------------
# FONCTIONS


def itinerary_extract(startpoint,endpoint,mode = "walking",waypoints = '',optimize_waypoints = False,language = "French"):
    '''Fonction qui extrait un chemin depuis google maps en fonction d'un point de départ et d'arrivée et de points
    intermédiaires'''

    if waypoints != '':
        waypoints_coord = [x['location'] for x in waypoints]    #adresses que l'on fournit à googlemaps
        waypoints_id = [x['id'] for x in waypoints]             #ids des waypoints correspondants que l'on conserve tout au long de l'algorithme
        waypoints_rating = [x['rating'] for x in waypoints]      #rating utilisateur pour l'algorithme
    else:
        waypoints_coord = ''
        waypoints_id = 0
        waypoints_rating = 0
    print('Itinerary Extraction')
    return (gmaps.directions(                               #appel à l'API directions googlemaps
                startpoint,                                 #point de départ (addresse ou coordonnées)
                endpoint,                                   #point d'arrivée
                mode = mode,                                #mode de transport ('walking','driving','bicycling')
                departure_time = datetime.now(),            #faire l'appel au moment actuel
                waypoints = waypoints_coord,                 #points intermédiaires de passage, peut être vide
                optimize_waypoints = optimize_waypoints,    #permet de tracer le chemin optimal entre les points intermédiaires
                language = language                         #renvoie les résultats dans la langue appropriée
                ),
            waypoints_id,
            waypoints_rating)

    
def distance_matrix(startpoint,endpoint,mode="walking"):
    '''Fonction pour faire un appel à l'API Distance Matrix plus légère'''
    return gmaps.distance_matrix(startpoint,endpoint,mode = mode,departure_time = datetime.now())



def hms_to_s(hours,minutes = 0,seconds = 0):
    '''Convertit une durée en heures minutes secondes en secondes'''
    return hours*3600 + minutes*60 + seconds

def s_to_hms_text(seconds):
    '''convertit une durée en secondes en une durée heures minutes secondes en texte'''
    hours = floor(seconds/3600)
    left = seconds%3600
    minutes = floor(left/60)
    seconds = left%60
    if seconds > 30:
        minutes +=1
    return str(hours)+" h "+str(minutes)+" min"
    

from math import radians, cos, sin, asin, sqrt #fonctions nécessaires pour faire des calculs trigonométriques
def haversine(lng1, lat1, lng2, lat2):
    '''formule permettant de trouver la distance entre deux points connaissant leurs coordonnées géographiques''' 
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2]) #convertir les angles degrés en radians
    # formule d'Haversine 
    dlng = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c                                                   #6367 correspond au rayon terrestre moyen
    return km                                                       #Renvoie la valeur en km




def itinerary_parameters(itinerary):
    '''Extrait les paramètres intéressants d'un appel google maps à Directions fourni par la fonctions 'itinerary_extract' sous format json'''
    waypoints_id = itinerary[1]
    waypoints_rating = itinerary[2]
    itinerary = itinerary[0]
    legs = itinerary[0]['legs'] #les legs d'un itinéraire sont les sous-itinéraires entre les points intermédiaires

    #Créer un dictionnaire contenant les paramètres que l'on voudra utiliser dans les algorithmes ou l'affichage
    parameters = {'duration':0, #initialiser la durée totale de trajet à 0
                  'distance':0, #initialiser la distance parcourue à 0
                  
                   #initialiser une liste contenant tous les points de l'itinéraire (startpoint,waypoints,endpoint)
                  'points':[{'location':legs[0]['start_location'],  #coordonnées géographiques
                             'duration':0,                          #durée pour aller jusqu'à ce point + durée pour aller jusqu'au point d'après
                             'name':legs[0]['start_address']}],     #addresse du point
                  'waypoint_order':itinerary[0]['waypoint_order'],  #ordre des points rendu par l'optimiseur de googlemaps
                  'overview_polyline':itinerary[0]['overview_polyline']['points'].replace('\\','\\\\'), #code correspondant au tracé de l'itinéraire qui sera utilisé dans l'affichage de la carte - replace \\ -> \\\\ permet de corriger le problème d'encodage de \ en string python
                  'bounds':itinerary[0]['bounds']}                  #récupère les bordures Nord Est et Sud Ouest de l'itinéraire, ce qui permet un bon centrage de la carte lors de l'affichage
    #Construction pour chaque portion d'itinéraire   
    for i in range(0,len(legs)):
        leg = legs[i] 
        duration_leg = leg['duration']['value']
        parameters['duration'] += duration_leg                      #rajoute à la durée totale de trajet la durée de la branche
        parameters['distance'] += leg['distance']['value']          #rajoute à la distance totale parcourue la distance de la branche
        parameters['points'] += [{'location':leg['end_location'],'duration':duration_leg,'name':leg['end_address']}] #rajoute un nouveau point correspond au point de fin de la branche en récupérant ses coordonnées, son nom et la durée pour aller jusqu'à ce point (durée avant)
        parameters['points'][i]['duration'] += duration_leg         #rajoute à la durée du point précédent la durée de la branche de telle sorte que ce paramètre contienne la durée pour aller jusqu'à ce point + la durée pour aller de ce point au point suivant de l'itinéraire
    
    #Sépare la liste des points de l'itinéraire en point de départ, point d'arrivée, points intermédiaires
    parameters['startpoint'] = parameters['points'][0]
    parameters['endpoint'] = parameters['points'][-1]
    parameters['waypoints'] = parameters['points'][1:-1]
    waypoints_id = [waypoints_id[i] for i in parameters['waypoint_order']] #on reprend bien les ids correspondants aux waypoints dans le bon ordre fourni par 'waypoint_order'
    waypoints_rating = [waypoints_rating[i] for i in parameters['waypoint_order']] #idem pour les rating
    #définit le centre de l'itinéraire pour calculer l'éloignement de chaque point par rapport au centre, en moyennant les coordonnées du point de départ et d'arrivée
    center = {'lat': (parameters['startpoint']['location']['lat']+parameters['endpoint']['location']['lat'])/2,
              'lng': (parameters['startpoint']['location']['lng']+parameters['endpoint']['location']['lng'])/2}  
    
    #Construction des scores d'intérêts pour passer par un point intermédiaire
    if len(parameters['waypoints'])>0: #s'il existe des points intermédiaires
        for i in range(0,len(parameters['waypoints'])):
            waypoint = parameters['waypoints'][i]
            #on définit l'éloignement par rapport au centre spatial de l'itinéraire grâce à la fonction prenant en paramètre les coordonnées géographiques
            #Ceci permet d'avoir une donnée sur l'éloignement à vol d'oiseau quand le critère 'duration' donne une notion d'éloignement en durée au sein de l'itinéraire
            #D'autre part utiliser les coordonnées déjà présentes dans les paramètres permet de limiter les appels à l'API google maps
            waypoint['remoteness'] = haversine(waypoint['location']['lng'],waypoint['location']['lat'],center['lng'],center['lat'])
            waypoint['id'] = waypoints_id[i]
            waypoint['rating'] = waypoints_rating[i]
    
        #Trouve le maximum des critères d'intérêts définis plus tôt afin de pouvoir normaliser le score d'intérêt
        max_duration = max(parameters['waypoints'],key = lambda t:t['duration'])['duration']
        max_remoteness = max(parameters['waypoints'],key = lambda t:t['remoteness'])['remoteness']
    
        #Pour chaque point intermédiaire on construit un score pour chaque critère et un score moyen qui servira à éliminer ce point dans l'algorithme de choix des points de passage
        for waypoint in parameters['waypoints']:
            waypoint['score'] = {}
            waypoint['score']['duration'] = 1-(waypoint['duration']/max_duration)       #score normalisé
            waypoint['score']['remoteness'] = 1-(waypoint['remoteness']/max_remoteness) #score normalisé
            waypoint['score']['rating'] = waypoint['rating']/10                       #score normalisé sur un rating maximal de 10
            
            #Prend l'ensemble des scores définis et prend une moyenne pondérée qui permet d'utiliser tous ces critères en même temps
            # Le modèle ici prend pour importance :
            # - 40% pour l'éloignement en durée 
            # - 40% pour l'éloignement spatial
            # - 20% pour le rating du lieu donné par les utilisateurs
            waypoint['score']['total'] = (0.4 * waypoint['score']['duration'])+(0.4 * waypoint['score']['remoteness']+(0.2*waypoint['score']['rating']))

    return parameters #Renvoie l'ensemble de ces paramètres 
    

#-----------------------------------------------------------------------------
# Extraction depuis les paramètres créés par la fonction 'itinerary_parameters'    

def duration_value(parameters):
    '''Renvoie la durée totale en valeur'''
    return parameters['duration']

def duration(parameters):
    '''renvoie la durée totale en texte'''
    value = duration_value(parameters)
    return s_to_hms_text(value)
    
def distance_value(parameters):
    '''renvoie la distance totale en valeur'''
    return parameters['distance']

def distance(parameters):
    '''renvoie la distance totale en texte'''
    value = distance_value(parameters)
    return str(round(value/1000,1))+" km"

    
def geo_waypoints(parameters):
    '''renvoie une liste des coordonnées des points de passage'''
    return [x['location'] for x in parameters['waypoints']]

    
def geocoding(point):
    '''réalise un appel à google maps pour connaitre les coordonnées d'un point'''
    return gmaps.geocode(point)[0]['geometry']['location']

def coords(point):
    '''Renvoie les coordonnées d'un point sous forme d'un couple (abscisse, ordonnée)'''
    x = float(geocoding(point)['lat'])
    y = float(geocoding(point)['lng'])
    return (x,y)

#===========================================================================================================
#Algorithme d'optimisation du passage

'''@author: Orso-Manuel'''

# Fonctions géométriques

def nodeDistance(node1, node2):
    '''Renvoie la distance entre deux noeuds'''
    (x1, y1) = node1
    (x2, y2) = node2
    d=((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
    return d

def midDistance(node1, node2, node3):
    '''Renvoie la distance de node2 au segment [node1, node3]'''
    (x1, y1) = node1
    (x3, y3) = node3
    center = ((x1+x3)/2, (y1+y3)/2)
    return nodeDistance(node2, center)     

def isInDisk(node1, node2, node3):
    '''Renvoie True ssi node2 se situe dans le disque de diamètre [node1, node3]'''
    node2 = (node2['lat'],node2['lng'])
    radius = nodeDistance(node1, node3)/2
    return midDistance(node1, node2, node3) <= radius



# Algorithme de suppression d'un waypoint
def remove_remote(waypoints):
    '''Supprime de l'itinéraire le noeud ayant le score (distance + rating le plus faible)'''
    position = waypoints.index(min(waypoints,key = lambda t:t['score']['total']))
    return waypoints[:position]+waypoints[position+1:]

# Algorithme de calcul des waypoints
def optimization_algo_1(startpoint, endpoint, mode, duration_request, waypoints):
    '''Renvoie le chemin optimisé passant par le maximum de points en une durée impartie'''

    '''1. Délimitation du périmètre'''
    itinerary = itinerary_extract(startpoint, endpoint, mode)
    parameters = itinerary_parameters(itinerary)
    start = (parameters['startpoint']['location']['lat'],parameters['startpoint']['location']['lng'])
    end = (parameters['endpoint']['location']['lat'],parameters['endpoint']['location']['lng'])
    (lng1, lat1) = start
    (lng2, lat2) = end
    if duration_value(parameters) < duration_request/2:
        #Si le point de départ et le point d'arrivée sont identiques
        if start == end:
            lng1 += 0.001
            lng2 -= 0.001
            itinerary = itinerary_extract((lng1, lat1), (lng2, lat2), mode, '')
            parameters = itinerary_parameters(itinerary)
        distance_request = duration_request*distance_value(parameters)/duration_value(parameters)
        #Tant que la distance entre les points de départ et d'arrivée est trop petite
        #Augmenter le diamètre de recherche des points
        while haversine(lng1, lat1, lng2, lat2)*1000 < 2*distance_request:
            lng1 += 0.005
            lng2 -= 0.005
    new_start = (lng1, lat1)
    new_end = (lng2, lat2)
    new_center = ((lng1+lng2)/2,(lat1+lat2)/2)

    '''2. Tri des monuments situés dans le périmètre'''
    #On fixe la liste des monuments à considérer à l'intérieur du disque de diamètre (new_start, new_end)

    all_waypoints = []
    for monument in waypoints:
        if isInDisk(new_start, monument['location'], new_end):
            location = list(monument['location'].values())
            new_monument = monument
            new_monument['remoteness'] = nodeDistance(new_center,location)
            all_waypoints += [new_monument]

    if len(all_waypoints) > 0:
        max_remoteness = max(all_waypoints,key = lambda t:t['remoteness'])['remoteness']
        for waypoint in all_waypoints:
            waypoint['score'] = 0.2*(waypoint['rating']/10) + 0.8*(1-waypoint['remoteness']/max_remoteness)

    #Calcul initial pour réperer et classifier les monuments identifiés dans le périmètre 

    all_waypoints = sorted(all_waypoints,key = lambda t:t['score'],reverse = True)
    all_waypoints = all_waypoints[:23]

    '''3. Ajout de waypoints à l'itinéraire, par groupes de 5'''
    j = 5
    waypoints = all_waypoints[0:j] #id et adresse des étapes de l'itinéraire - on limite à 28 pour ne pas faire planter l'API
    print(len(all_waypoints))
    itinerary = itinerary_extract(startpoint, endpoint, mode, waypoints, True, 'French')      #calcule l'itinéraire passant par les points de passage obtenus
    parameters = itinerary_parameters(itinerary)                                                #extrait les paramètres du précédent itinéraire
    waypoints = parameters['waypoints']
    print('1')
    #Tant que la durée cumulée entre les points de passage est inférieure à la moitié de la durée imposée
    #On ajoute 5 points de passage
    while (duration_value(parameters) < duration_request and j != len(all_waypoints)):
        j += 5
        if j > len(all_waypoints):
            j = len(all_waypoints)
        waypoints = all_waypoints[0:j]
        itinerary = itinerary_extract(startpoint, endpoint, mode, waypoints, True)
        parameters = itinerary_parameters(itinerary)
        
    message = ""                                                                        #définit un message qui pourra être affiché en fonction des conditions
    bounds = parameters['bounds']                                                       #définit les limites de la carte qui seront récupérées pour l'affichage
    waypoints = parameters['waypoints']


    '''4. Correction éventuelle de l'itinéraire'''
    #Tant que la durée de l'itinéraire est supérieure à la durée de la balade demandée, on enlève des points de passage        
    while (duration_value(parameters) > duration_request and len(waypoints) > 1):    #la liste doit contenir plus d'un point de passage
        waypoints = remove_remote(waypoints)
        itinerary = itinerary_extract(startpoint, endpoint, mode, waypoints, True)                                           #on recalcule l'itinéraire avec les nouveaux points de passage                         
        parameters = itinerary_parameters(itinerary)                                        #on recalcule les paramètres du nouvel itinéraire
        bounds = parameters['bounds']
        waypoints = parameters['waypoints']

    #Si la durée de l'itinéraire est inférieure à la durée demandée
    if duration_value(parameters) <= duration_request:
        print("Allright")
        print(all_waypoints)
        print(parameters['waypoints'])
        print('Trip duration:', s_to_hms_text(duration_value(parameters)))
        print('Requested trip duration:', s_to_hms_text(duration_request))
        return (parameters, all_waypoints, message, bounds)                              #on renvoie ces paramètres à la fin de la boucle si un itinéraire avec au moins un point de passage a été trouvé

    #Si l'itinéraire ne peut comporter aucun point de passage
    else:
        itinerary = itinerary_extract(startpoint, endpoint, mode, '')                                          #on recalcule l'itinéraire avec les nouveaux points de passage
        parameters = itinerary_parameters(itinerary)                                        #on recalcule l'itinéraire sans points de passage

        #L'itinéraire direct départ->arrivée est acceptable
        if duration_value(parameters) <= duration_request:
            print("You cannot visit but you still can go straight to the arrival.")
            print("It would take you " + s_to_hms_text(duration_value(parameters)))
            return (parameters, all_waypoints, message, bounds)
        
        #L'itinéraire départ->arrivée est déjà trop long
        else:
            print("It is impossible to do what you ask for.")
            print("Actually the trip would take you at least " + s_to_hms_text(duration_value(parameters)) + '.')
