'''import requirements'''
from flask import Flask, jsonify, request, abort, render_template, redirect
from flask import url_for, session
from flask_cors import CORS
import json
import os
import jwt
import base64
from models import setup_db, Providers, Events, Customers, db
from auth import AuthError, requires_auth
from functools import wraps


'''set up the app with Flask and data-base'''
app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, PUT, POST, PATCH, DELETE, OPTIONS')
    return response


'''HOME ROUTE'''


@app.route('/')
def index():
    a = 'https://val1.eu.auth0.com/authorize?audience=image&'
    b = 'response_type=token&client_id=86sK45Zcy75vaACB1EsJB12hFbUGBT68&'
    c = 'redirect_uri=http://127.0.0.1:5000/'
    x = 'https://val1.eu.auth0.com/v2/logout?'
    y = 'client_id=86sK45Zcy75vaACB1EsJB12hFbUGBT68'
    return render_template('index.html', login=a+b+c, logout=x+y)


@app.route('/logout')
def loginout():
    return redirect(url_for('index'))


'''IMPLEMENT PROVIDER(S) CLASS ROUTES'''
'''get all providers'''


@app.route('/providers', methods=['GET'])
def providers():
    response = {}
    cityes = []
    # get all the cityes
    city = db.session.query(Providers.city).distinct().order_by('id').all()
    for a in city:
        # for every city get all the providers
        v = Providers.query.filter(Providers.city == a[0]).order_by('id').all()
        # append those providers on a list
        providers = []
        for b in v:
            providers.append(b.format())
        # for every city append city name and the providers list
        cityes.append({'city': a[0], 'providers': providers})
    response['cityes'] = cityes
    # return response body
    response['success'] = True
    return jsonify(response)


'''post a new provider '''
# here we need to implement 2 routes:
# one for sending the user to page hosting the form


@app.route('/providers', methods=['PUT'])
@requires_auth('post:providers')
def providers_form_page(payload):
    a = request.json['token']
    token = base64.b64decode(str(a).split(".")[1]+"==")
    return jsonify({'success': True,
                    'token': str(token),
                    'redirect': 'post_providers'})


@app.route('/post_providers')
def post_pro():
    return render_template('post_providers.html')


# second for the post implementation, for handle user imput


@app.route('/providers', methods=['POST'])
@requires_auth('post:providers')
def post_providers(payload):
    response = {}
    # get and check the user imput
    body = request.get_json()
    if body:
        name = body.get('name')
        services_offered = body.get('services_offered')
        city = body.get('city')
        adress = body.get('adress')
        phone = body.get('phone')
        website = body.get('website')
        social_media = body.get('social_media')
        image_link = body.get('image_link')
        events = body.get('events')
        if name and city and adress and phone and social_media and image_link:
            provider = Providers(id=None, name=name,
                                 services_offered=services_offered,
                                 city=city, adress=adress, phone=phone,
                                 website=website,
                                 social_media=social_media,
                                 image_link=image_link)
        else:
            abort(400)
        # insert provider data into db
        if provider:
            provider.insert()
            response['success'] = True
            response['id'] = provider.id
            response['redirect'] = 'providers'
            provider.sesion_close()
        else:
            abort(400)
    else:
        abort(400)
    # return the response
    return jsonify(response)


'''delete a provider'''


@app.route('/providers/<int:id>', methods=['DELETE'])
@requires_auth('delete:providers')
def delete_provider(payload, id):
    response = {}
    # get and check provider id and retrievment from db
    provider = Providers.query.get(id)
    if provider:
        provider.delete()
        response['success'] = True
        response['deleted id:'] = provider.id
        # close the session
        provider.sesion_close()
    else:
        abort(404)
    # return respond
    response['success'] = True
    return jsonify(response)


'''edit a provider'''


@app.route('/providers/<int:id>', methods=['PATCH'])
@requires_auth('edit:providers')
def edit_provider(payload, id):
    response = {}
    # get and check the provider retrievment from db
    provider = Providers.query.get(id)
    if provider:
        # get and check the user imput data
        body = request.get_json()
        if body:
            for x in body.keys():
                if x in provider.format().keys():
                    for y in provider.format().keys():
                        if x == y:
                            # a = f'{x}'
                            # customer.a = str(body[x])
                            # print(customer,customer.a,a,str(body[x]))
                            # check rows meant to be modified and insert them
                            if body.get('name'):
                                provider.name = body['name']
                            if body.get('services_offered'):
                                a = body['services_offered']
                                provider.services_offered = a
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
                            # asign new data to respond body and close session
                            response['provider'] = provider.format()
                            response['body'] = body
                else:
                    abort(400)
        else:
            abort(400)
    else:
        abort(404)
    # close the session
    provider.sesion_close()
    # return response body
    response['success'] = True
    return jsonify(response)


'''retrieve a single provider'''


@app.route('/providers/<int:id>', methods=['GET'])
def provider(id):
    response = {}
    events = []
    # get and check provider retrieve from db
    provider = Providers.query.get(id)
    if provider:
        # asign it to response body
        response['provider'] = provider.format()
    else:
        abort(404)
    # retrieve the provider's events with asigned customers from db tables
    a = Events.query.filter_by(provider_id=id).join('providers').join('customers').all()
    # format and asign events to response body
    for x in range(len(a)):
        events.append({'event_name': a[x].event_name,
                       'event_type': a[x].event_type,
                       'date_time': a[x].date.isoformat(),
                       'customer name': a[x].customers.name,
                       'customers_image_link': a[x].customers.image_link})
    response['provider'].update({'events': events})
    # return response body
    response['success'] = True
    return jsonify(response)


'''search for provider(s)'''


@app.route('/providers', methods=['PATCH'])
def search_providers():
    response = {}
    results = []
    count = 0
    # get and check the user imput data
    body = request.get_json()
    if body.get('searched_term'):
        # append searched term to respond body
        searched_term = request.json['searched_term']
        response['searched_term'] = searched_term
        # retrieve the results from db and append them to a results list
        res = Providers.query.filter(Providers.name.ilike(f'%{searched_term}%'))order_by('id').all()
        for a in res:
            count += 1
            results.append(a.format())
        response['counts'] = count
        response['results'] = results
    else:
        abort(400)
    # return the respond
    response['success'] = True
    return jsonify(response)


'''IMPLEMENT CUSTOMER(S) CLASS ROUTES'''
'''get all customers'''


@app.route('/customers', methods=['GET'])
def customers():
    response = {}
    cityes = []
    # get all the cityes
    city = db.session.query(Customers.city).distinct().order_by('id').all()
    for a in city:
        # for every city get all the customers
        v = Customers.query.filter(Customers.city == a[0]).order_by('id').all()
        # append those providers on a list
        customers = []
        for b in v:
            customers.append(b.format())
        # for every city append city name and the providers list
        cityes.append({'city': a[0], 'customers': customers})
    response['cityes'] = cityes
    # return response body
    response['success'] = True
    return jsonify(response)


'''post a new customer'''
# here we need to implement 2 routes :
# one for sending the user to page hosting the form


@app.route('/customers', methods=['PUT'])
@requires_auth('post:customers')
def customers_form_page(payload):
    a = request.json['token']
    token = base64.b64decode(str(a).split(".")[1]+"==")
    return jsonify({'success': True,
                    'token': str(token),
                    'redirect': 'post_customers'})


@app.route('/post_customers')
def post_cus():
    return render_template('post_customers.html')


# second for the post implementation for handle user imput
@app.route('/customers', methods=['POST'])
@requires_auth('post:customers')
def post_customers(payload):
    response = {}
    # get and check the user imput
    body = request.get_json()
    if body:
        name = body.get('name')
        city = body.get('city')
        adress = body.get('adress')
        phone = body.get('phone')
        social_media = body.get('social_media')
        image_link = body.get('image_link')
        if name and city and adress and phone and social_media and image_link:
            customer = Customers(id=None, name=name, city=city, adress=adress,
                                 phone=phone, social_media=social_media,
                                 image_link=image_link)
        else:
            response['success'] = False
            abort(400)
        # inser provider data into db
        if customer:
            customer.insert()
            response['success'] = True
            response['id'] = customer.id
            response['redirect'] = 'customers'
            customer.sesion_close()
        else:
            abort(400)
    else:
        abort(400)
    # return the response
    return jsonify(response)


'''delete a customer '''


@app.route('/customers/<int:id>', methods=['DELETE'])
@requires_auth('delete:customers')
def delete_customer(payload, id):
    response = {}
    # get and check provider id and retrievment from db
    customer = Customers.query.get(id)
    if customer:
        customer.delete()
        response['success'] = True
        response['deleted id:'] = customer.id
        # close the session
        customer.sesion_close()
    else:
        abort(404)
    # return respond
    return jsonify(response)


'''edit a customer'''


@app.route('/customers/<int:id>', methods=['PATCH'])
@requires_auth('edit:customers')
def edit_customer(payload, id):
    response = {}
    # get and check the customer retrievement from db
    customer = Customers.query.get(id)
    if customer:
        # get and check the user imput data
        body = request.get_json()
        if body:
            for x in body.keys():
                if x in customer.format().keys():
                    for y in customer.format().keys():
                        if x == y:
                            # a = f'{x}'
                            # customer.a = str(body[x])
                            # print(customer,customer.a,a,str(body[x]))
                            # check rows meant to be modified and asign them
                            if body.get('name'):
                                customer.name = body['name']
                            if body.get('city'):
                                customer.city = body['city']
                            if body.get('adress'):
                                customer.adress = body['adress']
                            if body.get('phone'):
                                customer.phone = body['phone']
                            if body.get('social_media'):
                                customer.social_media = body['social_media']
                            if body.get('image_link'):
                                customer.image_link = body['image_link']
                            if body.get('events'):
                                customer.events = body['events']
                            customer.update()
                            # asign new data to respond body
                            response['body'] = body
                            response['customer'] = customer.format()
                            response['success'] = True
                else:
                    abort(400)
        else:
            abort(400)
    else:
        abort(404)
    customer.update()
    # close the session
    customer.sesion_close()
    # return response body
    return jsonify(response)


'''retrieve a customer'''


@app.route('/customers/<int:id>', methods=['GET'])
def customer(id):
    response = {}
    events = []
    # get and check customer retrieve from db
    customer = Customers.query.get(id)
    if customer:
        response['customer'] = customer.format()
    else:
        abort(404)
    # retrieve the customer events with asigned provider from db tables
    a = Events.query.filter_by(customer_id=id).join('providers').join('customers').all()
    for x in range(len(a)):
        events.append({'event_name': a[x].event_name,
                       'event_type': a[x].event_type,
                       'date_time': a[x].date.isoformat(),
                       'provider name': a[x].providers.name,
                       'provider_image_link': a[x].providers.image_link})
    # format and asign events to response body
    response['customer'].update({'events': events})
    # return response body
    response['success'] = True
    return jsonify(response)


'''search for customer(s)'''


@app.route('/customers', methods=['PATCH'])
def search_customers():
    response = {}
    results = []
    count = 0
    # get and check the user imput data
    body = request.get_json()
    if body:
        if body.get('searched_term'):
            # append shearched term to respond body
            searched_term = body.get('searched_term')
            response['searched_term'] = searched_term
            # retrieve the results from db and append them to a result list
            res = Customers.query.filter(Customers.name.ilike(f'%{searched_term}%')).all()
            for a in res:
                count += 1
                results.append(a.format())
            response['count'] = count
            response['results'] = results
        else:
            abort(400)
    else:
        abort(400)
    response['success'] = True
    # return response body
    return jsonify(response)


'''IMPLEMENT EVENTS CLASS ROUTES'''
'''get all events'''


@app.route('/events', methods=['GET'])
def events():
    response = {}
    # retrieve all the events from db
    events = Events.query.all().order_by('id').all()
    response['events'] = [a.format() for a in events]
    # return response body
    response['success'] = True
    return jsonify(response)


'''post a new event'''
# here we need to implement 2 routes :
# one for sending the user to page hosting the form


@app.route('/events', methods=['PUT'])
@requires_auth('post:events')
def events_form_page():
    return jsonify({'message': 'here is route for the page hosting the form'})


# second for the post implementation for handle user imput
@app.route('/events', methods=['POST'])
@requires_auth('post:events')
def post_eevnt(payload):
    error = False
    response = {}
    # get and check the user imput
    try:
        body = request.get_json()
        event_name = body.get('event_name')
        event_type = body.get('event_type')
        date = body.get('date')
        rating = body.get('rating')
        provider_id = body.get('provider_id')
        customer_id = body.get('customer_id')
        # if event_name and event_type and date:
        event = Events(id=None, event_name=event_name, event_type=event_type,
                       date=date, rating=rating, provider_id=provider_id,
                       customer_id=customer_id)
        # inser event data into db
        event.insert()
        response['success'] = True
        response['id'] = event.id
        event.sesion_close()
    except BaseException:
        abort(400)
    # return the response
    return jsonify(response)


'''delete a event'''


@app.route('/events/<int:id>', methods=['DELETE'])
@requires_auth('delete:events')
def delete_event(payload, id):
    response = {}
    # get and check event id and retrievment from db
    event = Events.query.get(id)
    if event:
        event.delete()
        response['success'] = True
        response['deleted id'] = event.id
        # close the session
        event.sesion_close()
    else:
        abort(404)
    # return respond
    return jsonify(response)


'''edit a event'''


@app.route('/events/<int:id>', methods=['PATCH'])
@requires_auth('edit:events')
def edit_event(payload, id):
    response = {}
    # get and check the event retrievement from db
    event = Events.query.get(id)
    if event:
        # get and check the user imput data
        body = request.get_json()
        if body:
            for x in body.keys():
                if x in event.format().keys():
                    for y in event.format().keys():
                        if x == y:
                            # a = f'{x}'
                            # customer.a = str(body[x])
                            # print(customer,customer.a,a,str(body[x]))
                            # check rows meant to be modified and asign them
                            if body.get('event_name'):
                                event.event_name = body['event_name']
                            if body.get('event_type'):
                                event.event_type = body['event_type']
                            if body.get('date'):
                                event.date = body['date']
                            if body.get('rating'):
                                event.rating = body['rating']
                            if body.get('customer_id'):
                                event.customer_id = body['customer_id']
                            if body.get('provider_id'):
                                event.provider_id = body['provider_id']
                            event.update()
                            # asign new data to respond body
                            response['success'] = True
                            response['event'] = event.format()
                else:
                    abort(400)
        else:
            abort(400)
    else:
        abort(404)
    # close the session
    event.sesion_close()
    # return response body
    return jsonify(response)


'''retrieve a event'''


@app.route('/events/<int:id>', methods=['GET'])
def event(id):
    response = {}
    # get and check event retrieve from db
    event = Events.query.get(id)
    if event:
        response['event'] = event.format()
    else:
        abort(404)
    # return response body
    response['success'] = True
    return jsonify(response)


'''IMPLEMENT ERRORS HANDELERS ROUTES'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

@app.errorhandler(401)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 400

@app.errorhandler(403)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Forbiden'
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


@app.errorhandler(405)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405


@app.errorhandler(422)
def unprocesable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocesable Entity'
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Server Error'
    }), 500


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
