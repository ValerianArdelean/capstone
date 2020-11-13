# Immage Service API

### Introduction
Welcome to my final project for the Udacity's [Full Stack Web Developer Nanodegree course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).
Image Service is meant to be a virtual place for where customers can meet providers in the imagery field industry, designated for private events like weddings, etc.

### Overview
 * The app is build using RESTful API's principles, serving three (main) resources: ```/providers```, ```/customers``` and ```/events```.
 * Each main resource that groups data, branch to individual resource accessed by id.
 * The app have build a partial front end - the home route - and two out of three the post forms are served by UI.
 * All others resources can be C.R.U.D. using http protocol with appropriate **methods**, **headers** and **jsonify bodies**.
 * All of the responses are returned in jsonify form, even the responses requested in UI pages.
     *  Exception from that are the following routes:
       ```
       (/) # return the home HTML format page,
       (/logout) # return to home.
       (/post_providers) # return the providers post HTML form
       (/post_customers) # return the customers post HTML form
       ```

### Authentication - role permissions and usage:
This app is designed to work with guests users and logged in users.
* Guests users can read, search, and access all resources.
* Logged in users can perform CRUD operations, based on they role permissions.\
  They are 2 roles implemented already: '''provider''' and '''customer'''
    1. provider role have the following permissions:
  ```
    [  "post:events",
        "delete:events",
        "edit:events",
        "post:providers",
        "delete:providers",
        "edit:providers"    ]
  ```
    2. customer role have the following permissions:
  ```
   [  "post:customers",
        "delete:customers",
        "edit:customers",
        "edit:events"       ]
  ```
* The sign up process is not implemented, however two email addresses that had been already assigned with the one role, are provided:
    - barista_shop@aol.com - have the permissions for the customer role
    - manager_shop@aol.com - have the permissions for the provider role
    - - both email addresses share the same password : baristA1234
* Sign in/out buttons are provided in the UI home page.\
Once you logged with one of the email addresses, you can C.R.U.D a provider or a customer(yourself) and events.
    (One provider can have multiple customers, thru events, and vice versa)
* Authentication is implemented using third part Auth0 system and ends up with a JWT delivered into home page url as query parameter.
You can also grab the token from the console log, witch u can access using web browser dev tools. If JWT is not showed in console log, a page refresh should work. From there you can copy your JWT for further purposes like testing or performing C.R.U.D. operations in the protected routes.
Or you can carry on by hitting one of the POST buttons available in the home page UI - In this case you don-t have to copy or save token.


### Getting Started
* install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

* Set up a virual enviornment.\
  To do that follow [oficial instructions from python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
  or use these commands:
  ```
  $ python3 -m venv env
  $ source env/bin/activate
  ```

* [Fork](https://github.com/ValerianArdelean/capstone) and and clone your forked repository to your machine.
  Work on the project locally and make sure to push all your changes to your remote repository

* [Install Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

* [SQLAlchemy](https://www.sqlalchemy.org/) is library to handle the interaction between Flask server and data-base.

* [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

* Install all others dependencies:
  ```
  $ pip3 install -r requirements.txt
  ```
* Export app env variables
  ```
  $ source setup.sh
  ```
* Run the development server:
  ```
  $ export FLASK_ENV=development # enables debug mode # create errors if test_config file runs with this evn. var. exported
  $ flask run # to run after installing dependences
  ```
* Navigate to Home page [http://localhost:5000](http://localhost:5000)\
  On this stage, home route can run with no errors, however, if you click on any resource links, app will fail, as no db system have been implemented. Follow the next section steps to implement a database system.


### Database
* This app have been created and tested using a Postgresql database system\
 **Please instal PostgreSQL and Psycopg2**\
After succesfuly installation, make sure postgres server is up and running:
```
$ pg_ctl -D /usr/local/var/postgres start
```
* To create the database use the following command in CLI:
```
$ createdb capstone-ardelean
```
* To reset the database, delete and create the data-base:
```
$ dropdb && createdb capstone-ardelean
```
* To create data-base tables, columns and relations you can use 2 options:

     1. Use dedicated migrations file: ```manage.py```
            * In CLI run the following command :
              ```
              $ python3 manage.py db migrate
              $ python3 manage.py db upgrade
              ```
  If any errors occur, you my consider one of the following 2 options: <p> First, delete the migrations folder, then initiate again: In CLI, prior above step run: ```$ python3 manage.py db init``` - this will initiate migrations folder.\
  Or, you can use stamp head command. Same, prior the migrate comands above, in CLI run: ```$ python3 manage.py db stamp head```

  2. Use the restore data-base file provided. In CLI run: ```$ psql capstone-ardelean < capstone-test.sql``` \
  This will create table tables and relations exacly like migrations run, but will also fill the db tables with some dummy data.


### Files Project Structure
    ```sh
    ├── app.py *** The controler.
    ├── manage.py *** Adaptor for the database migration script to run on Heroku
    ├── test_config.py *** Unittest and integration tests.
    ├── auth.py *** The JWT digest module
    ├── models.py *** SQLAlchemy db models.
    ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
    ├── setup.sh *** Enviroment variables like Database URL, JWT secret, etc.
    ├── capstone-test.sql *** Test-database restore file(can be used and to create main db)
    ├── CAPSTONE.postman_collection.json *** Postman integration test collection runner
    ├── README.md *** Current readme file
    ├── Procfile *** Heroku file
    │
    ├── migrations
    │   ├── alembic.ini
    │   ├── env.py
    │   ├── README
    │   ├── script.py.mako
    │   └── versions
    │       ├── ....
    │       └── d1b59e6a4e8f_.py
    │
    ├── static
    │   ├── script.js *** javascript code for getting the token
    │   └── css
    │       └── main.css *** css code for style the home page
    │
    └── templates
        ├── index.html *** home page
        ├── post_customers.html *** serving the post providers form
        ├── post_providers.html *** serving the post customers form
        └── layouts
            └── main.html *** layout for the HTML pages
    ```


### Resources Endpoints
  All endpoints:
  ```
  GET '/providers'
  PUT '/providers'
  GET '/post_providers'
  POST '/providers'
  DELETE '/providers/<int:id>'
  PATCH '/providers/<int:id>'
  GET '/providers/<int:id>'
  PATCH '/providers'

  GET '/customers'
  PUT '/customers'
  GET '/post_customers'
  POST '/customers'
  DELETE '/customers/<int:id>'
  PATCH '/customers/<int:id>'
  GET '/customers/<int:id>'
  PATCH '/customers'

  GET '/events'
  PUT '/events'
  POST '/events'
  DELETE '/events/<int:id>'
  PATCH '/events/<int:id>'
  GET '/events/<int:id>'
  ```

All endpoints with explanations:
```
-PROVIDERS-
-get all providers-
GET '/providers'
- Request Arguments: None
- Response is a jsonify dictionary having providers filter_by by cityes with main keys 'success' and 'cityes'
      Key 'success' have a boolean value
      key 'cityes' have a list of dictionaryes, each having keys 'city' and 'providers'
      key 'city' have value a string meaning a city name
      key providers have value a list of dictionaryes.
{
  "cityes": [
    {
      "city": "Arad",
      "providers": [
        {
          "adress": "Str. Ardealului No. 3A",
          "city": "Arad",
          "id": 3,
          "image_link": "imagine",
          "name": "Ardelean Valerian",
          "phone": "+40",
          "services_offered": "photography",
          "social_media": "http://www.facebook.com",
          "website": "http://www.google.com"
        },
        {
          "adress": "Str. Ardealului No. 3A",
          "city": "Arad",
          "id": 4,
          "image_link": "imagine",
          "name": "Ardelean Valerian",
          "phone": "+40",
          "services_offered": "photography",
          "social_media": "http://www.facebook.com",
          "website": "http://www.google.com"
        }
      ]
    },
    {
      "city": "Timisoara",
      "providers": [
        {
          "adress": "Str.Romantei No. 5",
          "city": "Timisoara",
          "id": 5,
          "image_link": "imagine",
          "name": "ofelia IOana",
          "phone": "+40",
          "services_offered": "photography",
          "social_media": "http://www.facebook.com",
          "website": "http://www.google.com"
        }
      ]
    }
  ],
  "success": true
}
- Errors : - 405 if wrong HTTP method


-post a provider-
PUT '/providers'
- Request Arguments: - an 'Authorization' header having as value a Bearer JWT token with the 'post:providers' permission.
- Response is a jsonify dictionary having 2 keys: 'success' and 'redirect'.
      key redirect have value a string, meaning the function desired to be redirected
{
  "redirect": "post_providers",
  "success": true
}
- Errors : - 401 if token is missing
           - 403 if permissions not found in token
           - 405 if wrong HTTP method


-post a provider-
GET '/post_providers'
- Request Arguments: - None
- Return an HTTP page hosting post for for providers


-post a provider-
POST '/providers'
- Request Arguments: - an 'Authorization' header having as value a Bearer JWT token with the 'post:providers'       permission.
                      - a json body having following keys: name, services_offered,
city, adress, phone, website, social_media, image_link.
                     {
                       "name": "string",
                       "services_offered": "string",
                       "city":"string",
                       "adress":"string",
                       "phone":"string",
                       "website":"string",
                       "social_media":"string",
                       "image_link":"string"
                      }
- Response is a jsonify dictionary having 3 keys : id, redirect, success.
       key redirect have value a string, meaning the function desired to be redirected
       key id have value a int, meaning the id provider id inserted
{
    "id": 6,
    "redirect": "providers",
    "success": true
}
- Errors : - 400 if wrong keys are inserted
           - 401 if token is missing
           - 403 if permissions not found in token
           - 405 if wrong HTTP method


-delete a provider-
DELETE '/providers/<int:id>'
- Request Arguments: - integer id in the query url
                     - an 'Authorization' header having as value a Bearer JWT token with the 'delete:providers' permission.
- Response is a jsonify dictionary having 2 keys : deleted id, success.
{
  "deleted id:": 6,
  "success": true
}
- Errors : - 401 if token is missing
           - 403 if permissions not found in token
           - 404 if wrong provider id inserted
           - 405 if wrong HTTP method


-edit a provider-
PATCH 'providers/<int:id>'
- Request Arguments: - an 'Authorization' header having as value a Bearer JWT token with the 'edit:providers' permission.
                     - integer id in the query url
                     - json object having as keys at least one of the entryes desired to be edited. Example: {
                                                  "name": "matcha shake",
                                                  "city":"patchTESTEDCITY"
                                                  }

- Response is a jsonify dictionary having 2 json objects separated by comma and one success key.
First dictionary reprezent the desired fields in db to be edited. Second object is the final edited provider.
{
"body": {
"city": "patchTESTEDCITY",
"name": "matcha shake"
},
"provider": {
"adress": "Str. Ardealului No. 3A",
"city": "patchTESTEDCITY",
"id": 3,
"image_link": "imagine",
"name": "matcha shake",
"phone": "+40",
"services_offered": "photography",
"social_media": "http://www.facebook.com",
"website": "http://www.google.com"
},
"success": true
}
- Errors : - 400 if wrong keys are inserted
           - 401 if token is missing
           - 403 if permissions not found in token
           - 404 if id from the query parameter not found
           - 405 if wrong HTTP method


-retrieve a single provider-
GET 'providers/<int:id>'
- Request Arguments: - integer id in the query url
- Response is a jsonify dictionary with 2 keys: provider and success. Provider key have as value another dictionary representing the provider data as bellow :
{
"provider": {
"adress": "Str. Ardealului No. 3A",
"city": "patchTESTEDCITY",
"events": [],
"id": 3,
"image_link": "imagine",
"name": "matcha shake",
"phone": "+40",
"services_offered": "photography",
"social_media": "http://www.facebook.com",
"website": "http://www.google.com"
},
"success": true
}
- Errors : - 404 if is wrong id in url


-search for provider(s)-
PATCH '/providers'
- Request Arguments: - a json body with a 'searched_term' key: {
    "searched_term": "ale"
}
- Response is a jsonify dictionary having 4 keys: counts, result, shearched_term and success: {
  "counts": 1,
  "results": [
    {
      "adress": "Str. Ardealului No. 3A",
      "city": "Arad",
      "id": 4,
      "image_link": "imagine",
      "name": "Ardelean Valerian",
      "phone": "+40",
      "services_offered": "photography",
      "social_media": "http://www.facebook.com",
      "website": "http://www.google.com"
    }
  ],
  "searched_term": "ale",
  "success": true
}
- Errors : - 400 if wrong keys are inserted
           - 405 if wrong HTTP method


For the customers resource Endpoints, the request arguments, responses and errors, mirror exactly the providers ones, except the path. All the paths for the customers resource can be found at the begin of this chapter.
In order to keep this README as DRY as possible, we will carry on with the events resource only.


-EVENTS-
-get all events-
GET '/events'
- Request Arguments: - None
- Response is a jsonify dictionary having 2 keys: events and success,
as follow : {
    "events": [],
    "success": true
}
- Errors : - 405 if wrong HTTP method


-post a new event-
POST '/events'
- Request Arguments: - an 'Authorization' header having as value a Bearer JWT token with the 'post:events'
                     - a json body having following keys: name, services_offered,
                      city, adress, phone, website, social_media, image_link.
                      {
                        "event_name":"photoshoot",
                        "event_type":"foto",
                        "date": "2020-03-04",
                        "rating": integer,
                        "provider_id": integer,
                        "customer_id": integer
                      }
- Response is a jsonify dictionary having 2 keys: id and success: {
  "id": 3,
  "success": true
}
- Errors : - 400 if wrong keys are inserted
           - 401 if token is missing
           - 403 if permissions not found in token
           - 404 if id from the query parameter not found
           - 405 if wrong HTTP method

-delete a event-
DELETE '/events/<int:id>'
- Request Arguments: - event id inserted as parameter in the url query
                     - an 'Authorization' header having as value a Bearer JWT token with the 'delete:events'
- Response is a jsonify dictionary having 2 keys: deleted id and success: {
    "deleted id": 3,
    "success": true
}          
- Errors : - 401 if token is missing
           - 403 if permissions not found in token
           - 404 if id from the query parameter not found
           - 405 if wrong HTTP method

-edit a event-
PATCH '/events/<int:id>'
- Request Arguments: - event id inserted as parameter in the url query
                     - an 'Authorization' header having as value a Bearer JWT token with the 'edit:events' permission
                     - a json body containing minimum one key from the post events json body requirements
                     {
                       "event_name": "Deane",
                       "rating":100
                     }
- Response is a jsonify dictionary having  2 keys : event and success. the event key have another json object,
representing the edited event:{
                              "event": {
                              "customer_id": null,
                              "date": "Wed, 04 Mar 2020 00:00:00 GMT",
                              "event_name": "Deane",
                              "event_type": "foto",
                              "id": 4,
                              "provider_id": null,
                              "rating": 100
                              },
                              "success": true
                              }
- Errors : - 400 if wrong keys are inserted
           - 401 if token is missing
           - 403 if permissions not found in token
           - 404 if id from the query parameter not found
           - 405 if wrong HTTP method


-retrieve a event-
GET '/events/<int:id>'
- Request Arguments: - event id inserted as parameter in the url query
- Response is a jsonify dictionary having 2 keys: success and event.
Event key have as value another dictionary representing the event with the id from the URL query parameter:
{
    "event": {
        "customer_id": null,
        "date": "Wed, 04 Mar 2020 00:00:00 GMT",
        "event_name": "Deane",
        "event_type": "foto",
        "id": 4,
        "provider_id": null,
        "rating": 100
    },
    "success": true
}
- Errors : - 404 if wrong id parameter in URL query is inserted
           - 405 if wrong HTTP method
```


### ERRORS RESPONSES
* The main errors have error handlers which return a jsonify body having 3 keys:
success, error and message.
```
    ({'success': False,
      'error': 400,
      'message': 'Bad Request'
    }), 400
```
The errors handled are : 400, 401, 403, 404, 405, 422, 500, JWTError, and AuthError.
I am not aware of any another errors this app my have, but in case you get some, these my come up as a http format message.


### TESTING
  * After you successfully build and run the app, and db tables was created, you can test the app either with POSTAN or either with Python UNITTEST library file provided.

    1. Testing using Postman:
        1. Download and install postman. [Follow instructions here](https://www.getpostman.com/) to install and run postman.  
        2. Once postman is running, import the collection ```CAPSTONE.postman_collection.json``` into the capstone app.
        3. Get the fresh tokens in postam enviroment:\
        Log in using the app provided UI. Use the provided email address ```manager_shop@aol.com``` with provided pass and log in. Copy the provided token(from the URL query parameter or from console-log (you can access using dev tools.)
        4. Update postman env variables.\
        To do so go to postman env icon, on there you will se the three env. variables postman is using it for testing this app : ```id```, ```provider_token``` & ```customer_token```. Click 'edit' and paste the token from u clipboard into provider_token fields.
        Log out from the app UI and repeat the step for the customer_token. For him log in using ```barista_shop@aol.com``` email address.\
        Attention: Both email addresses share the same password: ``` baristA1234``` !!!\
        Make sure the enviroment ```id``` variable is set to 1, especially if you start with fresh db.
        (The id env value update itself after each test run)\
        Click update and save all collection. Now you can run the collection.\
        If all steps above have been run successfully, no errors should arise during collection test.
        If any errors occur, make sure id value from env is set to reflect the real data-base id. If you not sure, dropdb & createdb using steps enumerated on Data-base section.
        5. You can use newman to run postman collection from the CLI. However a json file for handling env files and run it same time with collection, is not provided, and also take into consideration instaling newman.
    2. Testing using python unittest library:
       1. For the unittest run is better to restore the data-base from the provided sql file.
       This will insert some dummy data with id 1.
       2. Unittest library tests use os env variables. Please make sure they are updated and id vars reflect db reality.
       To do so open the ```setup.sh``` file. Update ``provider_token`` and ``customer_token`` values.
       Also make sure all ``customer_id``, ``provider_id`` and ``event_id`` **have value set to 2**(or reflect correct db reality). Save and exit.
       3. Open a new CLI tab or window and run the following command: ```$ source setup.sh```
       4. Run the test using : ```$ python3 test_config.py```.\
       If all the steps above have been done successfully, should run with no fails or errors.
       If any errors occur, make sure id in setup.sh have the proper value, and you source it into your enviroment prior test run.



### How to Contribute
* Contributions are welcome !
* In order to do so, first fork this repository to your account.
* Next, clone this repository to your machine, and then start to make changes.
  ```$ git clone {YOUR_REPOSITORY_CLONE_URL}
  ```
* create a new branch
* make commits
* make sure u catch the latest work from origin repository into yours before creating pull req. :
```#Create upstream as our repository
    $ git remote add upstream https://github.com/ValerianArdelean/capstone
   #rename branches  
    $ git remote rename mine origin
    $ git remote rename source-repo upstream
   # Fetch upstream changes in local machine:
    $ git fetch upstream master
   # Switch to master branch
    $ git checkout master
   # Merge changes to your master
    $ git merge upstream/master
```
* Push changes to your forked GitHub repository
  ```$ git push (-f) origin master
  ```
* make pull request
  - go to u forked repro and click on NEW PULL REQUEST button.
  - then select u branch
  - then click on CREATE PULL REQ


### License
The contents of this repository are covered under the [MIT License.](https://github.com/ValerianArdelean/capstone/blob/master/LICENSE)
