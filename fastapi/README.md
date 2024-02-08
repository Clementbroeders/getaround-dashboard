# DEPLOIEMENT FASTAPI

FastAPI est dépoyé sur un serveur RENDER et HEROKU (backup). 

Le déploiement est fait automatiquement à partir de GitHub (HEROKU : répertoire défini via le fichier `heroku.yml`)


## DEPLOIEMENT LOCAL

1) Build image

    `docker build -t fastapi .`

2) Run container

    `docker run -it -v "$(pwd):/home/app" -p 4000:4000 fastapi`


## RENDER LINK

[GetAround FastAPI Docs](https://getaround-fastapi.onrender.com/docs)


## HEROKU LINK

[GetAround Fastapi Docs](https://getaround-fastapi1-f159113e9f42.herokuapp.com/docs)


## PUSH TO HEROKU (VIA CLI)

Il est également possible de déployer FastAPI directement via HEROKU CLI avec les commandes suivantes :

1)  Connection Heroku

    `heroku container:login`

2) Push container to Heroku

    `heroku container:push web -a getaround-fastapi1`

3) Release container to Heroku

    `heroku container:release web -a getaround-fastapi1`

4) Open app

    `heroku open -a getaround-fastapi1`