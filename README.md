#TruckLog-Pro
Backend - ELD & HOS Engine
Le backend est une API REST robuste construite avec Django et Django REST Framework. Il sert de cerveau pour le calcul des itinéraires, la gestion des heures de service (HOS) et la génération automatique des journaux de bord électroniques (ELD).

🛠 Technologies utilisées
Framework : Django 5.x & Django REST Framework (DRF)

Authentification : JWT (Simple JWT)

Base de données : PostgreSQL (ou SQLite en développement)

Services Externes : API de Géocodage et OSRM/Google Maps pour le calcul d'itinéraires.

🌟 Fonctionnalités Clés
1. Moteur de calcul HOS (Hours of Service)
Calcule automatiquement les limites de conduite basées sur les régulations FMCSA :

Limite de conduite de 11 heures.

Pause obligatoire après 8 heures.

Calcul du cycle restant et détection des violations.

2. Générateur de logs ELD automatique
Dès qu'un voyage (Trip) est créé, le backend génère des objets LogDay contenant des segments de 24 heures.

Statuts gérés : OFF DUTY, ON DUTY, DRIVING, SLEEPER.

Précision : Les segments sont calculés pour couvrir exactement 1440 minutes (24h) afin d'assurer un rendu fluide de la courbe sur le frontend.

3. Géocodage et Itinéraires
Conversion des noms de villes en coordonnées GPS.

Récupération de la Polyline pour l'affichage de la carte côté client.

Calcul de la distance totale et de la durée estimée du trajet.

📂 Structure du Projet Backend
/models.py : Définition des trajets, des segments ELD et des profils chauffeurs.

/views.py : Logique de création des trajets avec génération automatique des logs à la volée.

/hos_engine.py : Algorithme de calcul des heures de service.

/eld_engine.py : Transforme les données de trajet en segments temporels pour le graphique.

🚦 Installation Rapide
Accéder au dossier : cd backend

Installer les dépendances : pip install -r requirements.txt

Lancer les migrations : python manage.py migrate

Démarrer le serveur : python manage.py runserver 8088
