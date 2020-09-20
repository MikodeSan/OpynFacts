# Web Application Deployment

## Environment

In order to separate deployment to development settings, a _settings_ module is defined where the default settings for development are placed into the ___init__.py_.
A _production.py_ can contain all the development settings and redefine some constant values.  
The private CONSTANT values (secret key, database credential, static files configuration, etc.) are defined in a _envar.py_ that is not tracked by _git_.  
By moving the setttings files, the application directory path is also redefine:  
`BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`

## Continuous integration

Connected to the GitHub account, [Travis](https://docs.travis-ci.com/user/languages/python) is configured to build tests on the specified repository branch.
The _.travis.yml_ define the Django settings module to the Travis settings file and the chome driver to use for tests:
`- google-chrome-stable --headless --disable-gpu --remote-debugging-port=9222 https://www.chromestatus.com &`

### set production setting / separate environment / env. variable

Modification du fichier de configuration
Set config file for prod
database

## Deployment

### Host

From [DigitalOcean](https://www.digitalocean.com), an Infrastructure as a Service (IAAS), a virtual/cloud server is rented and used to host the web application.
The aim is to be able to install every required software tool according to the system administrator's needs.

#### Server Configuration

A server space, also called ___Droplet___ by DigitalOcean, is created by defining the operating system distribution, the memory and computer ressources: Linux Ubuntu 20.04 (LTS) x64, 1 shared CPU, 1 GB RAM, 25 GB SSD Disk, 1000 GB bandwidth for data transfer.  
To be nearest to the end-users' localization, London is selected as the server location.
<!-- * An __image__ which is the Operating System distribution to install. Linux _Ubuntu 20.04 (LTS) x64_ is selected.
* __Memory and computer ressources__ where the number of CPU, RAM size, Disk size and bandwidth for data transfer are chosen according to the application expected performances. The selected configuration is 1 shared CPU, 1 GB RAM, 25 GB SSD Disk, 1000 GB transfer.
* An extra __Block storage__ can be added but it is not usefull for our web application.
* The __Server Localization__ is chosen in order to be nearest to the end-users's localization. So London is a good place. -->

To remote control the server, a previously [generated SSH public key](#ssh-key-gen) is also defined. <!-- (#ssh-keys-generation) -->

Finally, a firewall is added and defining InBound rules allowing ssh, http and https incoming traffic

### Host server remote control

Using MS Windows, the SSH connection is performed with __[PuTTY](https://putty.org)__. The same [operations](https://openclassrooms.com/fr/courses/43538-reprenez-le-controle-a-laide-de-linux/41773-la-connexion-securisee-a-distance-avec-ssh#/id/r-41601) are also available using __[OpenSSH](https://www.openssh.com)__ with a Linux distribution.

<!-- #### SSH keys generation -->
#### <a name='ssh-key-gen'></a>SSH keys generation

_Putty_ allows to [generate](https://openclassrooms.com/fr/courses/43538-reprenez-le-controle-a-laide-de-linux/41773-la-connexion-securisee-a-distance-avec-ssh#/id/r-2283022) private and public keys using _Puttygen_. A __passphrase__ is defined with private key for more security.  
Besides, the format used by _PuTTYGen_ for the public key is incompatible with _OpenSSH_ on Linux servers, so a fix is described int a this [article](https://www.digitalocean.com/docs/droplets/how-to/add-ssh-keys/create-with-putty/#working-with-puttys-public-key-format).

#### Authentication

With _PuTTY_, [authentication and connection](https://openclassrooms.com/fr/courses/43538-reprenez-le-controle-a-laide-de-linux/41773-la-connexion-securisee-a-distance-avec-ssh#/id/r-2283082) to the remote host server is performed by first defining the related private key location on the administration machine and the login username and IP address of the host server. Then, as the public key is defined on the host server we connect to this last one as ___root___ by running `root@ipaddress` command and specifying the _passphrase_.

In second, in order to preserve host server integrity, we define a _user_ with restricted action compared with _root_ and assign the ssh public key to this user. The login username is also set in _PuTTY_ session configuration to perform connection by `user@ipaddress` command.

<!-- L'agent SSH Pageant
programme retenir votre clé privée. ne demandera la passphrase qu'une fois au début -->

### Web application installation

<!-- #### Application installation -->
First, the libraries for _python_ and _PostgreSQL_ (database management) are installed.

* `sudo apt-get install python3-pip python3-dev libpq-dev virtualenv postgresql postgresql-contrib`

The application is downloaded from [repository](https://github.com/MikodeSan/OpynFacts) hosted on Github, then the virtual environnement is installed with the application requirements into the application directory.

<!-- #### Database installation -->
Being logged in as administrator to the database management system, the application database and an assigned user are created according to the defined _Django_ [production settings]().
The database can be defined by Django with a _migration_ command: `python manage.py migrate` and initialized if necessary by a _load data_ command `python manage.py loaddata application_dump.json`.  
Finally a _super user_ is created by `python manage.py createsuperuser`.

<!-- #### Generate static file -->
The static files need to be generated for the production settings:  
```
$ export ENV=PRODUCTION
$ python manage.py collectstatic
```

### Web server

<!-- #### HTTP server: NGINX -->

<!-- Directives pour Nginx -->
[Nginx](https://www.nginx.com) is used as HTTP server to provide the static files and redirect requests to the Django web application. The configuration and installation is described in this [article](https://openclassrooms.com/fr/courses/4425101-deployez-une-application-django/4688553-utilisez-le-serveur-http-nginx).

#### Web application server: Gunicorn

##### supervisor

[Gunicorn](https://gunicorn.org) is define as wsgi application service and _supervisor_ is the service to reload gunicorn if necessary.
<!-- gunicorn disquaire_project.wsgi:application
reload service automaticaly -->

## Monitoring

### Server ressources and performances

Once the application is online, it is interesting to monitore the host server state. _DigitalOcean_ providing monitoring service, some thresholds can be defined to alert by sending an e-mail in case of insufficient performance or ressources.
<!-- [NewRelic](https://newrelic.fr) -->

### Logging

[Sentry](https://sentry.io) is used as a dashbord to display all errors and logs of the Django web appication. After having created a Sentry project, the related token defined into the production settings file as ___Sentry DSN___ value. The level of logs is also set to `INFO` in order to collect by _Sentry_ some events as request for a product that is not already strored in the database.

```python
sentry_logging = LoggingIntegration(
    level=logging.DEBUG,        # Capture info and above as breadcrumbs
    event_level=logging.INFO  # Send errors as events
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration(), sentry_logging],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
```

## Automation

With the Linux __crontab__ aplication, a cron job is defined to run every week an update of the product database from [Openfoodfact](https://world.openfoodfacts.org):  
`0 2 * * 2 sh /path/to/app/zcronjob.sh`  
The script defines `PRODUCTION` as environment variable and the product update command to execute:
`/path/to/app/venv/bin/python /path/to/app/manage.py initializedatabase 0 >> /tmp/djg_opnfct_cron_sh.log`

## Domain Name

[IP address](https://134.209.185.7): 134.209.185.7
