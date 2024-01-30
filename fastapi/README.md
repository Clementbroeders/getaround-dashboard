# DEPLOIEMENT FASTAPI

FastAPI est dépoyé sur un serveur HEROKU. 

Le déploiement est fait automatiquement à partir de GitHub (répertoire défini via le fichier `heroku.yml`)


## HEROKU LINK

[GetAround Fastapi Docs](https://getaround-fastapi1-f159113e9f42.herokuapp.com/docs)


## PUSH TO HEROKU (CLI)

1)  Connection Heroku

    `heroku container:login`


2) Push container to Heroku

    `heroku container:push web -a getaround-fastapi1`


3) Release container to Heroku

    `heroku container:release web -a getaround-fastapi1`


4) Open app

    `heroku open -a getaround-fastapi1`