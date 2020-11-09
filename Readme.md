# Immage Service API

### Introduction
Welcome to my final project for the Udacity's [Full Stack Web Developer Nanodegree course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).
Image Service is meant to be a virtual place for where customers can meet providers in the imagery field industry, designated for private events like weddings, etc.

### Overview
The app is build using RESTful API's principles, serving three main resources: Providers, customers and events.
It have build a partial front end. The home route and two of the post forms are served by UI.
All others resources can be C.R.U.D. using http protocol with appropriate methods, headers and jsonify bodies.
All of the responses are returned in jsonify form, even the responses requested in UI pages.
        Exception from that are the following routes: (/) -render the home page,
                                                      (/logout)- redirect to home,
                                                      (/post_providers) render the providers post form
                                                      (/post_customers) render the customers post form
### Authentication
Beside the guests users, this app is implemented to work with 2 roles : provider
                                                                        customer
Log in/out buttons are provided in the UI home page.
Once you logged you can C.R.U.D a provider or a customer(yourself) and events.
    (One provider can have multiple customers thru events and vice versa)
Authentication is implemented using third part Auth0 system.
* The sign up process is not implemented, however two email addresses that have assigned already with the two roles are provided: - barista_shop@aol.com - is the replacement for customer role
              - manager_shop@aol.com - is the replacement for provider role
                    password for both email addresses is : baristA1234
Without being authenticated the post provider and customer buttons are not working.
* authentication process ends up with a JWT delivered into home page url or in the console log, witch u can access using web page dev tools.
  If JWT is not showed in console log, a page refresh should work.
From there you can copy your JWT for further purposes like testing or performing C.R.U.D. operations, or you can carry on by hitting one of the POST buttons available in the home page UI.
Guests users can read and search only.




### Development Setup

  First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask).

    ```
    $ cd ~
    $ sudo pip3 install Flask
    ```

  To start and run the local development server,

  1. Initialize and activate a virtualenv:
    ```
    $ cd YOUR_PROJECT_DIRECTORY_PATH/
    $ virtualenv --no-site-packages env
    $ source env/bin/activate
    ```

  2. Install the dependencies:
    ```
    $ pip install -r requirements.txt
    ```

  3. Run the development server:
    ```
    $ export FLASK_APP=myapp
    $ export FLASK_ENV=development # enables debug mode
    $ python3 app.py
    ```

  4. Navigate to Home page [http://localhost:5000](http://localhost:5000)
