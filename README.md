# OpynFacts Application

## Context

This is the documentation of the project __Open Food Facts Client__.  
The site "___Pur Beurre___" is a web application where the main goal is to find by one click, a healthy substitute for a food concidered too fat, too sweet, too salt.

## Packages / Epic

* __View__
  * Navigation
* __Account__
  * Authentification
  * Personal Space
* __Product__
  * Search
  * Recommendation
* __Non volatile memory__
  * Database
    * PostGreSQL

## Features (Release / Story)

### Use case / User story

#### Sequence

* As a user, I want to Initialize/Update database with French products coming from OpenFoodFacts
  * Initialize db
  * Download list of categories
  * Store categories into db
  * Download list of products for each specified category
  * Extract product data
  * Store only new product data
  * Set Category/Product Relation
  * Store Category/Product relation for only new relation 
  * Set db as completed

* As a user, I want to see all stored products by category
  * Populate/Display category list
  * Select all categories as default
  * Populate/Display products list
  * Select a set of category by clicking
  * Populate/Display products list related to selected category

* As a user, I want to Select a stored product and see its characteristics
  * Product Selection
  * Display Product description

* As a user, I want to find alternative product according to '_nutri score_' and '_nova_group_'
  * Check the categogy hierarchy where my selected product is included
  * Select a categogy to find an alternative product
  * Find a substitute under the same category
    * Get alternative food criteria by successive priority: '_nutri score_' then '_nova_group_'
  * Display alternative

* As a user, I want to store and restore my favorite alternative food/product
  * Set selected product as favorite by click on button '_>>_'
  * Populate/Display favorite list
    * Get all product set as favorite
  * Remove selected product from favorite list by click on button '_<<_'

<!--
* As a user, at first I want to get the categories list from Open Food Facts and secondly get the products list from the selected category.
  * Model
    * Get data from openXfacts site
      * use the openfoodfacts API
    * Get data from db
* As a user, I want to find alternative product according to __some criterias to define__
  * Check the categogy hierarchy where my selected product is included.
  * Select a categogy to find an alternative product.
* As a user, I want to store and restore my data into database
  * system use a MySQL DB
    * Create db
    * Initialize db
      * Store categories data into db
* As a user, I want to use a GUI to interact with db

### tasks

* sub-task

## Algorithm

## Workflow

* Activity diagram
* Processus

## Difficulty

* Solution

-->

## Architecture

### Front-end

#### HTML / CSS: Content and layout

- __Header__: Displays Logo, title and pickupline
- __Central zone__:
  - The _Dialog box_ is a void zone displaying messages from Grand-Py and the user.
    - Loader (Spinner) is an infinite loop animation coordinated by `keyframes`. The animation will be started and interrupted asynchronously according to HTTP request states.
  - The _Query field_ is compound of a text input to type a query and a submit button to validate the user's query.
- __Footer__: Lists the author's name and links to contact, source code (Github repository), project planning and social networks.
- __Responsiveness__: Maximal and minimal blocks size are defined and CSS `flex` property is used to stretch block if necessary.

#### JavaScript: Dynamic update of the application view and interface (data exchange) with the back-end

On submit event (~~enter key pressed or submit image click~~), the user's query is catched from input form and displayed into the dialog box as a text block. The `innerHTML` method is used to update the view content without refresh the web page.
Then, a spinner animation is started to simulate Grand-Py's reflection at the same time the query is sent as form data to the flask server via a AJAX post request.

When the response is received asynchronously from the server, a callback function extracts the received JSON-formatted data and displays the Grand-Py's reply and the defined map if necessary into the dialog box.

### Back-end (model)

#### Class diagram (Functional model)

##### Interface

#### Component

#### Deployment

#### Query analysis: identification of requested place

The goal is to identify the requested place from the user's query received from the front-end side.  
The punctuations signs defined in the python `string` class and the most common [_French_ stop words](https://github.com/6/stopwords-json/blob/master/dist/fr.json) are discarded from the sentence. In addition, a list of specific stop words such as [_adresse_, _situe_, _où est_, _trouve_, _cherche_, _aller_, _connais_, ...] are defined to delimit text block that could be a requested place.
Finally, the only one remaining text block is considered as the searched location. If more than one text block are remaining, a random pre-defined Grand-Py's reply is returned to the front-end, telling the query is not understood.

#### Localization of a specified place/site

#### Geocoding

The [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding) is used to locate the identified place.  
The place name is sent to the geocoding service via a HTTP request, as a result the standard address and the coordinates (longitude/latitude) are returned as JSON-formatted data.
In order to improve localization result, taking into account that the user is French, the local language as '_french_' and the preferential search region as ccTLD code '_fr_' are also specified to the service.

#### Map

Knowing the geocode (coodinates), the relative map can be got by sending a HTTP request to the [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static). By specifying to the service some parameters like image size, zoom level and coordinates of the pin, as a result the image URL of a static map (non-interactive) is returned.  
Then this URL can be transfered to the front-end side without the Google key for security.

#### Media Wiki

The geocode is also used to get back from [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page) the descritption of points of interest near the place. By sending to the service a HTTP `GET` request as `query` operation, and specifying the _coordinates_ and the _maximal perimeter_, a list of Wikipedia page identifiers is returned sorted by distance from specified coordinates.  
So, a random page can be selected in order to return Grand-Py's replies more diversified for the same user's query.

With another request speciying the selected _page identifier_, the page text of the point of interest is returned. So, by discarding titles, the first sentences are extracted and used to complete the Grand-Py's reply to the user.

#### Random reply

For each Grand-Py's reply, predefined text is randomly selected to embellish information returned to the user.


### Database interface

<!--
#### Hosting

- As a user, I want to  > Prod
  - configure heroku
  - variable d'environnement : clé google

## Intégration continue

Tests unitaires
- mock
couverture
linter
-->
<!-- 
## Installation

### Virtual environment

- Create virtual environment named '_venv_' for example
- Activate the new environment
- Install requirements from '_requirements.txt_'

### Start

```Python
python run.py
``` 
-->

## Installation

### Database
* Download and install MySQL
* Create database '__openfacts__' 
* Create user '_app_' with password '_No@app23_' on localhost with GRANT ALL PRIVILEGES on '__openfacts__' database 

### Virtual environment
* Create virtual environment named '_env_' for example
* Activate the new environment
* install requirements from '_requirements.txt_'

### Run application
execute : python '_opynfacts.py_'

## Resources

* [Web application](https://z-pur-beurre.herokuapp.com)
* [Planning P05](https://trello.com/b/LZOSEDow/opynfacts)
* [Planning P08](https://www.pivotaltracker.com/n/projects/2436156)
* [Source Code](https://github.com/MikodeSan/OpynFacts)

## Legal notices / Credits

Open Food Facts is the exclusive source of the data, any additions will be shared and back to the community under the OdBL licence.
