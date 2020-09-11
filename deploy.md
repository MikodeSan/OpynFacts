# Web Application Deployment


## Continuous integration

execution des test avant chaque push
Alert si echec 
[Travis](https://docs.travis-ci.com/user/languages/python)

screen shot of config

## Deployment

### Host: [DigitalOcean](https://www.digitalocean.com)

#### Droplet Creation

Image : Digital Ocean peut installer, à votre place, le système d'exploitation de votre choix.

Taille : caractéristiques du serveur à réserver. Vous choisissez l'espace alloué à votre application : la mémoire vive (CPU), la RAM et la bande passante. Sélectionnez l'option la moins chère pour l'exercice.

Ajouter un bloc de stockage : laissez vide, vous n'en avez pas besoin.

Localisation des serveurs : sélectionnez Amsterdam ou Londres. Le serveur doit être le plus proche possible des utilisateurs finaux.


#### Remote connection

SSH server

[IP address](https://134.209.185.7) of APP


## Monitoring

### [Sentry](https://sentry.io)

### [NewRelic](https://newrelic.fr/)


## Automation

### Cronjob

#### Crontab


## Domain Name

