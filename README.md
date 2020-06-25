# OpynFacts Application

## Context

This is the documentation of the project __Open Food Facts Client__.  
The site "___Pur Beurre___" is a web application where the main goal is to find by one click, a healthy substitute for a food concidered too fat, too sweet, too salt.

## Packages / Epic

Considering the main features and the potential reusability, the project is divided in two parts.

### Account administration (Authentification management)

* __Sign-up__ is performed in 2 steps:
  * The user keys his e-mail as username. The username unicity is checked according to existing user data stored in database.
  * The password has to be keyed two times to be confirmed and validated.
* __Sign-in__: the user is identified with keyed username if this last one is already stored into database. The login operation succeeds according to the corresponding password, otherwise an error message is prompted.
* __Profil__ (i.e. Personal page) is enabled once signed-in. It shows the user data such as registration date, login date and e-mail.
* __Logout__ operation sets the session as anonymous.

### Product Management

* __Search__: To get a targeted product by 1 click, the user's query is got from the search bar and sent via a html post request to the server side.  
First, the search of the targeted product is performed from the application database. Each word of the query must be contained into either the brand field or the name field of a product stored into the database.  
Otherwise, according to [documentation](https://documenter.getpostman.com/view/8470508/SVtN3Wzy?version=latest#58efae40-73c3-4907-9a88-785faff6ffb1), a search is requested to the OpenFoodFacts service specifying the query via a ```GET``` request ([example for "confiture"](https://world.openfoodfacts.org/cgi/search.pl?search_terms=confiture&search_simple=1&action=process&json=true&sort_by=unique_scans)), in reply to the request, a list of products is returned into a formatted-JSON file.  
Finally, in both cases, the product with the biggest popularity value ```unique_scans_n```, is used as reference to find an alternative product with better nutrition score.
* __Recommendation__: The strategy is to find the best healthy aternative products by browsing, from children to parents, the categories hierarchy of the reference product.  
For each category, the grades repartition is got by a _drilldown search_ in order to limit the number of HTML requests, (see example for ['_chocolate-nuts-cookie-bars_' category](https://fr-en.openfoodfacts.org/category/en:chocolate-nuts-cookie-bars/nutrition-grades)).  
Then only for each identified grade from the category, products are extracted by an [advanced search](https://fr-en.openfoodfacts.org/cgi/search.pl?action=process&page=1&page_size=1000&sort_by=unique_scans&json=true&tagtype_0=categories&tag_contains_0=contains&tag_0=en%3Achocolate-nuts-cookie-bars&tagtype_1=nutrition_grades&tag_contains_1=contains&tag_1=d) request and next are sorted according to respective priority criteria: amount of healthy nutrients (```nutrition_grades```), the degree of processing of products (```nova_group```) and popularity (```unique_scans_n```). The most healthy are saved.
* __Favorite__: If authentified, user set a product as favorite by clincking an heart icon.
On HTML click event, the custom ```data-state``` attribute/property value is sent to javascript function that will notify the Django application backend via a AJAX POST request to modify the products database.
According to the asynchronously HTTP response, the icon view state is updated without refresh the web page.  
Favorite products are shown on the specific web page by extracting from database the identified user's products data.
* __Details__: An anonymous user can see more information about a product by clicking on its image. For each [product page](https://myuka.herokuapp.com/product/3017620422003/result/3017620422003/nutella), more information are indicated such as nutrients levels for 100 g (extracted from the [```nutrient_levels```](https://world.openfoodfacts.org/api/v0/product/3017620422003.json) dictionary) and the corresponding OpenFoodFacts product page link.

## Database

The database contains:

* The list of user's account using the default user model of ```Django```
* The list of all imported products from the OpenFoodFacts database

The database model define relationships such as each user has a list of their Searched products and a list of their Favorite products. In Addition, each searched product is linked to the determined Alternative products.   
```SQLite``` is used for developpement and ```PostGreSQL``` for production.

To generate and see the database model, first create the destination folder, then execute: ```python manage.py graph_models -a -g -o .\path\to\your\destination\graph.svg```.

### Iniatialization and update

The application database is first initialized and updated by adding only the new categories containing the most amount of products. The [list of all categories](https://world.openfoodfacts.org/categories.json) is dowloaded from OpenFoodFacts ([documentation](https://documenter.getpostman.com/view/8470508/SVtN3Wzy?version=latest#categories)).  
Moreover each existing products from the database are updated with data extracted from [OpenFoodFacts source](https://documenter.getpostman.com/view/8470508/SVtN3Wzy?version=latest#4a0c27c3-3abc-42c4-bf97-63f4e4108294).

Then, from each category downloaded from source at the first step, the most popular products sorted by popularity and the healthiest ones sorted by nutrition grade and nova score are added to database. For each new product added, their categories are also added to database.  
Finally label for each stored category is updated from OpenFoodFacts source.

## Setup

### Virtual environment

* Create virtual environment named '_venv_' for example
* Activate the new environment
* Install requirements from '_requirements.txt_'

### Database initialization

Execute : ```python manage.py initializedatabase 0```

### Run application locally

Execute : ```python manage.py runserver```

### Test and coverage

Tests use the chromium driver to manage Chrome browser.
Make sure that your browser is up-to-date then [download](https://chromedriver.chromium.org) the last stable release and copy the ```chromedriver.exe``` at the same level than your project directory.

Run tests by executing: ```pytest [-s] [-Wa] [--exitfirst] [--reuse-db] [-vv] --cov=./ --cov-report html```.

## Resources

* [Web application](https://myuka.herokuapp.com)
* [Planning P08](https://www.pivotaltracker.com/n/projects/2436156)
* [Source Code](https://github.com/MikodeSan/OpynFacts/tree/py08)

## Legal notices / Credits

OpenFoodFacts is the exclusive source of the data, any additions will be shared and back to the community under the OdBL licence.
As recommended by the [API Documentation](https://documenter.getpostman.com/view/8470508/SVtN3Wzy?version=latest#4a0c27c3-3abc-42c4-bf97-63f4e4108294), for READ operations, a User-Agent HTTP Header has to be added into request with the name of app, the version, system and a url (if any) in order not to be blocked by mistake.
