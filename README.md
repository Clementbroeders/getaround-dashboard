# Get-Around Dashboard

<img src="img/image.jpg" alt="Image" width="50%" height="50%">

## Introduction

Lors de l'utilisation de **Getaround**, les conducteurs réservent des voitures pour une période spécifique, allant d'une heure à plusieurs jours. Ils sont censés ramener la voiture à temps, mais il arrive de temps en temps que les conducteurs soient en retard pour la restitution.

Les retours tardifs lors de la restitution peuvent générer un **fort mécontentement** pour le conducteur suivant si la voiture était censée être relouée le même jour : le service client rapporte souvent des utilisateurs insatisfaits parce qu'ils ont **dû attendre que la voiture revienne de la location précédente**, voire des utilisateurs ayant dû **annuler leur location parce que la voiture n'a pas été restituée à temps**.

Pour atténuer ces problèmes, nous avons décidé de mettre en place un **délai minimum entre deux locations**. Une voiture ne sera pas affichée dans les résultats de recherche si les heures d'arrivée ou de départ demandées sont trop proches d'une location déjà réservée.

Cela résout le problème des retours tardifs, mais peut également potentiellement nuire aux revenus de Getaround/propriétaires : nous devons trouver le bon compromis.

Les objectifs sont : 

1) **Délai** : Quelle devrait être la durée minimale du délai ?

2) **Checkin** : Doivent-ils activer la fonctionnalité pour tous les checkin ? Ou uniquement pour les checkin Connect ?

Pour les aider à prendre la bonne décision, ils ont besoin d'informations basées sur leurs données. Je leur propose donc un **tableau de bord interactif**, qui sera consultable en ligne depuis un navigateur internet.


## Accès au Dashboard

Vous pouvez accéder aux dashboard depuis le lien suivant :

[GetAround dashboard](https://getaround-dashboard.streamlit.app/)

Vous pouvez accéder à la documentation du FastAPI au lien suivant :

[FastAPI docs](https://getaround-fastapi1-f159113e9f42.herokuapp.com/docs)


## Clone du repo

Pour cloner le repo, utilisez la commande suivante :

`git clone https://github.com/Clementbroeders/getaround-dashboard.git`


## Comment ça marche ?

A remplir


## Deploiement local

Si vous souhaitez déployer l'application en local, vous pouvez choisir parmi une des étapes suivantes :

1) Déployer Streamlit + FastAPI

    Il faut simplement lancer la commande `docker-compose up`

    Les sites seront accessibles aux liens :

    - [Streamlit](http://localhost:8501) : `http://localhost:8501`

    - [FastAPI](http://localhost:4000/docs) : `http://localhost:4000`

2) Deployer Streamlit uniquement

    Il faut lancer les 2 commandes suivantes :

    - Build l'image : `docker build -t getaround-streamlit .`

    - Run le container : `docker run -it -v "$(pwd):/home/app" -p 8501:8501 getaround-streamlit`

    Le streamlit sera accessible au lien :

    [Streamlit](http://localhost:8501) : `http://localhost:8501`

3) Deployer FastAPI uniquement

    Readme disponible dans le dossier suivant : [/fastapi](fastapi)


## Machine-Learning

Le modèle de machine-learning est disponible au chemin `src/model.pkl` avec le preprocesseur `src/preprocessor.pkl`.

Si vous souhaitez directement lancez vous-même le script (pour obtenir les métriques), vous pouvez lancer la commande suivante `python machine_learning.py`