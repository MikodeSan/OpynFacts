# Web Application Deployment


## Continuous integration

execution des test avant chaque push
Alert si echec 
[Travis](https://docs.travis-ci.com/user/languages/python)

screen shot of config

#### set production setting / separate environment / env. variable


## Deployment

### Host

An Infrastructure as a Service (IAAS) is rented and used as a virtual/cloud server to host the web application.
With this solution, every required software tool can be installed according to the system administrator's needs.  
The chosen IAAS is [DigitalOcean](https://www.digitalocean.com)

#### Server Configuration: Droplet

A server space, also called ___Droplet___ by DigitalOcean, is created and defined by:

* An __image__ which is the Operating System distribution to install. Linux _Ubuntu 20.04 (LTS) x64_ is selected.
* __Memory and computer ressources__ where the number of CPU, RAM size, Disk size and bandwidth for data transfer are chosen according to the application expected performances. The selected configuration is 1 CPU, 1 GB RAM, 25 GB SSD Disk, 1000 GB transfer.
* An extra __Block storage__ can be added but it is not usefull for our web application.
* The __Server Localization__ is chosen in order to be nearest to the end-users's localization. So London is a good place.

### SSH Remote connection

SSH server

#### Generate key

/!\ Be careful about generated key format uncompatible with linux server /!\ -> [solution](https://www.digitalocean.com/docs/droplets/how-to/add-ssh-keys/create-with-putty)

#### Connect with root

#### Connect with new user

### Install web application

#### set production setting / separate environment / env. variable

#### Install libraries

[IP address](https://134.209.185.7) of APP

#### Clone Git repository

#### Set virtual env and install requirement

#### Database

Create database

##### migrate django database

Configuration file
migrate command

loaddata
create superuser

#### Generate static file


### Web server

#### HTTP server: NGINX

Directives pour Nginx

Servir des fichiers statiques avec Nginx

Diriger le trafic vers une application Django

#### Web application server: Gunicorn

##### supervisor 
reload service automaticaly



## Monitoring

### Server ressources and performances

#### DigitalOcean monitoring

#### [NewRelic](https://newrelic.fr/)

### Logging 

#### [Sentry](https://sentry.io)



## Automation

### Cronjob

#### Crontab - django crontab


## Domain Name

NA