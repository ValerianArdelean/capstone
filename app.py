''' APP-CONTROLER MODULE'''

'''import requirements'''
from flask import Flask,render_template, jsonify,request,abort,redirect,url_for
from flask_cors import CORS
import json
'''import from models module'''
from models import setup_db, Providers, Events, Customers, db
'''set up the app with Flask and data-base'''
app = Flask(__name__)
setup_db(app)
db.init_app(app)

'''HOME ROUTE'''
@app.route('/')
def index():
    return jsonify('success':True)

'''IMPLEMENT PROVIDER(S) CLASS ROUTES'''
'''get all providers'''
@app.route('/providers', methods=['GET'])
def providers():
      cityes = []
      #get all the cityes
      city = db.session.query(Providers.city).distinct().all()
      for a in city :
          #for every city get all the providers
          v = Providers.query.filter(Providers.city==a[0]).all()
          #append those providers on a list
          providers = []
          for b in v :
              providers.append(b.format())
          #for every city append city name and the providers list
          cityes.append({'city':a[0],'providers':providers})
      #return response body
      return jsonify(cityes)

'''post a new provider '''
#here we need to implement 2 routes:
    #one for sending the user to page hosting the form
@app.route('/providers', methods=['PUT'])
def providers_form_page():
    return jsonify({'message':'here is the route for the host of the form'})

    #second for the post implementation, for handle user imput
@app.route('/providers', methods=['POST'])
def post_providers():
    response = {}
    #get and check the user imput
    body = request.get_json()
    if body :
        name = body.get('name')
        services_offered = body.get('services_offered')
        city = body.get('city')
        adress = body.get('adress')
        phone = body.get('phone')
        website = body.get('website')
        social_media = body.get('social_media')
        image_link = body.get('image_link')
        if name and city and adress and phone and social_media and image_link :
            provider = Providers(name=name,services_offered=services_offered,
                            city=city,adress=adress,phone=phone,website=website,
                                social_media=social_media,image_link=image_link)
        else:
            abort(400)
        #insert provider data into db
        if provider:
            provider.insert()
            response['success'] = True
            response['id'] = provider.id
            provider.sesion_close()
        else:
            abort(400)
    else:
        abort(400)
    #return the response
    return jsonify(response)

'''delete a provider'''
@app.route('/providers/<int:id>', methods=['DELETE'])
def delete_provider(id):
    response = {}
    #get and check provider id and retrievment from db
    provider = Providers.query.get(id)
    if provider:
        provider.delete()
        response['success'] = True
        response['deleted id:'] = provider.id
        #close the session
        provider.sesion_close()
    else:
        abort(404)
    #return respond
    return jsonify(response)

'''edit a provider'''
@app.route('/providers/<int:id>', methods=['PATCH'])
def edit_provider(id):
    respond = {}
    #get and check the user imput data
    body = request.get_json()
    if body:
        respond['body'] = body
    else:
        abort(400)
    #get and check the provider retrievment from db
    provider = Providers.query.get(id)
    if provider:
        #check rows meant to be modified and asign them to provider-s table in db
        if body.get('name') :
            provider.name = body['name']
        if body.get('services_offered'):
            provider.services_offered = body['services_offered']
        if body.get('city'):
            provider.city = body['city']
        if body.get('adress'):
            provider.adress = body['adress']
        if body.get('phone'):
            provider.phone = body['phone']
        if body.get('website'):
            provider.website = body['website']
        if body.get('social_media'):
            provider.social_media = body['social_media']
        if body.get('image_link'):
            provider.image_link = body['image_link']
        if body.get('events'):
            provider.events = body['events']
        provider.update()
        #asign new data to respond body and close the session
        respond['provider'] = provider.format()
        provider.sesion_close()
    else:
        abort(404)
    return jsonify(respond)

'''retrieve a single provider'''
@app.route('/providers/<int:id>', methods=['GET'])
def provider(id):
    #get and check provider retrieve from db
    provider = Providers.query.get(id)
    if provider :
        pass
    else:
        abort(404)
    #return the provider
    return jsonify({'provider':provider.format()})

'''search for provider(s)'''
@app.route('/providers',methods=['PATCH'])
def search_providers():
    results = []
    count = 0
    #get and check the user imput data
    body = request.get_json()
    if body.get('searched_term'):
        #append searched term to respond body
        searched_term = request.json['searched_term']
        #retrieve the results from db and append them to a results list
        res = Providers.query.filter(Providers.name.ilike(f'%{searched_term}%')).all()
        for a in res :
            count += 1
            results.append(a.format())
    else:
        abort(400)
    #return the respond
    return jsonify({'search_term':searched_term, 'counts':count, 'results':results })


'''IMPLEMENT CUSTOMER(S) CLASS ROUTES'''
'''get all customers'''
@app.route('/customers', methods=['GET'])
def customers():
      cityes = []
      #get all the cityes
      city = db.session.query(Customers.city).distinct().all()
      for a in city :
          # for every city get all the customers
          v = Customers.query.filter(Customers.city==a[0]).all()
          # append those providers on a list
          customers = []
          for b in v :
              customers.append(b.format())
          #for every city append city name and the providers list
          cityes.append({'city':a[0],'customers':customers})
      #return response body
      return jsonify(cityes)

'''post a new customer'''
#here we need to implement 2 routes :
    #one for sending the user to page hosting the form
@app.route('/customers', methods=['PUT'])
def customers_form_page():
    return jsonify({'message':'here is the route for the page hosting the form'})

    #second for the post implementation for handle user imput
@app.route('/customers', methods=['POST'])
def post_customers():
    response = {}
    #get and check the user imput
    body = request.get_json()
    if body :
        name = body.get('name')
        city = body.get('city')
        adress = body.get('adress')
        phone = body.get('phone')
        social_media = body.get('social_media')
        image_link = body.get('image_link')
        if name and city and adress and phone and social_media and image_link :
            customer = Customers(name=name,city=city,adress=adress,phone=phone,
                                social_media=social_media,image_link=image_link)
        else:
            abort(400)
        #inser provider data into db
        if customer:
            customer.insert()
            response['success'] = True
            response['id'] = customer.id
            customer.sesion_close()
        else:
            abort(400)
    else:
        abort(400)
    #return the response
    return jsonify(response)

'''delete a new customer '''
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    response = {}
    #get and check provider id and retrievment from db
    customer = Customers.query.get(id)
    if customer:
        customer.delete()
        response['success'] = True
        response['deleted id:'] = customer.id
        #close the session
        customer.sesion_close()
    else:
        abort(404)
    #return respond
    return jsonify(response)

'''edit a new customer'''
@app.route('/customers/<int:id>', methods=['PATCH'])
def edit_customer(id):
    respond = {}
    #get and check the user imput data
    body = request.get_json()
    if body:
        respond['body'] = body
    else:
        abort(400)
    #get and check the customer retrievement from db
    customer = Customers.query.get(id)
    if customer:
        #check rows meant to be modified and asign them to provider-s table in db
        if body.get('name') :
            customer.name = body['name']
        if body.get('services_offered'):
            customer.services_offered = body['services_offered']
        if body.get('city'):
            customer.city = body['city']
        if body.get('adress'):
            customer.adress = body['adress']
        if body.get('phone'):
            customer.phone = body['phone']
        if body.get('website'):
            customer.website = body['website']
        if body.get('social_media'):
            customer.social_media = body['social_media']
        if body.get('image_link'):
            customer.image_link = body['image_link']
        if body.get('events'):
            customer.events = body['events']
        customer.update()
        #asign new data to respond body and close the session
        respond['customer'] = customer.format()
        customer.sesion_close()
    else:
        abort(500)
    return jsonify(respond)

'''retrieve a customer'''
@app.route('/customers/<int:id>', methods=['GET'])
def customer(id):
    #get and check customer retrieve from db
    customer = Customers.query.get(id)
    if customer :
        pass
    else:
        abort(404)
    #return the customer
    return jsonify({'customer':customer.format()})

'''search for customer(s)'''
@app.route('/customers',methods=['PATCH'])
def search_customers():
    results = []
    count = 0
    #get and check the user imput data
    body = request.get_json()
    if body :
        pass
    else:
        abort(400)
    if body.get('searched_term'):
        #append shearched term to respond body
        searched_term = body.get('searched_term')
        #retrieve the results from db and append them to a result list
        res = Customers.query.filter(Customers.name.ilike(f'%{searched_term}%')).all()
        for a in res :
            count += 1
            results.append(a.format())
    else:
        abort(400)
    #return the respond
    return jsonify({'search_term':searched_term, 'counts':count, 'results':results })


@app.errorhandler(400)
def bad_request(error):
  return jsonify ({
    'success':False,
    'error':400,
    'message':'Bad Request'
    }),400

@app.errorhandler(404)
def not_found(error):
  return jsonify ({
    'success':False,
    'error':404,
    'message':'Not Found'
  }),404

@app.errorhandler(405)
def not_found(error):
  return jsonify ({
    'success':False,
    'error':405,
    'message':'Method Not Allowed'
  }),405

@app.errorhandler(422)
def unprocesable_entity(error):
  return jsonify ({
    'success':False,
    'error':422,
    'message':'Unprocesable Entity'
  }),422

@app.errorhandler(500)
def server_error(error):
  return jsonify ({
    'success':False,
    'error':500,
    'message':'Server Error'
  }),500
