# OpynFacts Application

This is the documentation of the project __Open Food Facts manager__

Open Food Facts is the exclusive source of the data, any additions will be shared and back to the community under the OdBL licence.

## Installation

### Database
* Download and install MySQL
* Create database '__openfacts__' 
* Create user '_app_' with password '_No@app23_' on localhost with GRANT ALL PRIVILEGES on '__openfacts__' database 

### virtual environment
* Create virtual environment named '_env_' for example
* Activate the new environment
* install requirements from '_requirements.txt_'

### Run application
execute : python '_opynfacts.py_'

## Features (Release / Story)

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

## Links

Trello: https://trello.com/b/LZOSEDow/opynfacts
Github: https://github.com/MikodeSan/OpyFoodFacts
