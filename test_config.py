import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import Providers, Customers, setup_db
from auth import AuthError, requires_auth


class TestProviders(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.database_path = 'postgresql://valerian@localhost:5432/capstone-test'
        setup_db(self.app, self.database_path)

        self.provider_token = os.environ['PROVIDER_TOKEN']
        self.provider_id = os.environ['provider_id']
        self.provider_header = {'Content-Type': 'application/json',
                                'Authorization': 'Bearer {}'.format(self.provider_token)}
        self.new_provider = {'name': 'NAME', 'services_offered':'services',
                             'city': 'CITY','adress': 'ADDRESS',
                             'phone': 'PHONE', 'website':'website',
                             'social_media': 'facemol', 'image_link': 'immage'}

        self.customer_token = os.environ['CUSTOMER_TOKEN']
        self.customer_id = os.environ['customer_id']
        self.customer_header = {'Content-Type': 'application/json',
                                'Authorization': 'Bearer {}'.format(self.customer_token)}
        self.new_customer = {'name': 'NAME', 'city': 'CITY','adress': 'ADDRESS',
                             'phone': 'PHONE', 'social_media': 'facemol',
                             'image_link': 'immage'}

        self.events_token = self.provider_token
        self.event_id = os.environ['event_id']
        self.new_event = {'event_name':'NAME', 'event_type': 'photo-video',
                          'date':'2020-03-05', 'rating': 9}

        with self.app.app_context():
             self.db = SQLAlchemy()
             self.db.init_app(self.app)
             self.db.create_all()

    def tearDown(self):
        pass

    '''Test home route for 200 & 404'''
    def test_get(self):
        res1 = self.client().get('/')
        self.assertEqual(res1.status_code, 200)
        res2 = self.client().get('/aur')
        self.assertEqual(res2.status_code, 404)

    '''Test get all providers routes'''
    def test_200_get_providers(self):
        res = self.client().get('/providers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cityes'])

    def test_404_get_providers(self):
        res = self.client().get('/providersMISSPEL')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''Test search for a provider'''
    def test_200_search_providers(self):
        res = self.client().patch('/providers',json={'searched_term':'are'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_search_providers(self):
        res = self.client().patch('/providers',json={'searched_MISSPEELL':'are'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    '''Test get for a specific provider'''
    def test_200_get_provider(self):
        res = self.client().get('/providers/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_provider(self):
        res = self.client().get('/providers/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_200_post_provider(self):
        res = self.client().post('/providers', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.provider_token)},
                                    json = self.new_provider)
        data = json.loads(res.data)
        print('inserted provider id',data['id'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_403_post_provider(self):
        res = self.client().post('/providers', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.customer_token)},
                                    json = self.new_provider)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_200_edit_provider(self):
        res = self.client().patch('/providers/1', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.provider_token)},
                                    json = {'name': 'EDITED NAME', 'city': 'EDIT CITY'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_edit_provider(self):
        res = self.client().patch('/providers/1', headers = {'Content-Type': 'application/json'},
                                    json = {'name': 'EDITED NAME', 'city': 'EDIT CITY'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    def test_200_delete_provider(self):
        res = self.client().delete('/providers/{}'.format(self.provider_id), headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.provider_token)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_provider(self):
        res = self.client().delete('/providers/203', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.provider_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)







    '''Test get all customers routes'''
    def test_200_get_customers(self):
        res = self.client().get('/customers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cityes'])

    def test_404_get_customers(self):
        res = self.client().get('/customersMISSPEL')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''Test search for a customer'''
    def test_200_search_customers(self):
        res = self.client().patch('/customers',json={'searched_term':'are'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_search_customers(self):
        res = self.client().patch('/customers',json={'searched_MISSPEELL':'are'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    '''Test get for a specific customer'''
    def test_200_get_customer(self):
        res = self.client().get('/customers/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_customers(self):
        res = self.client().get('/customers/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_200_post_customers(self):
        res = self.client().post('/customers', headers = {'Content-Type': 'application/json',
                                 'Authorization': 'Bearer {}'.format(self.customer_token)},
                                 json = self.new_customer)
        data = json.loads(res.data)
        print('inserted customer id', data['id'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_403_post_customer(self):
        res = self.client().post('/customers', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.provider_token)},
                                    json = self.new_provider)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_200_edit_customer(self):
        res = self.client().patch('/customers/1', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.customer_token)},
                                    json = {'name': 'EDITED NAME', 'city': 'EDIT CITY'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_edit_customer(self):
        res = self.client().patch('/customers/1', headers = {'Content-Type': 'application/json'},
                                    json = {'name': 'EDITED NAME', 'city': 'EDIT CITY'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_200_delete_customer(self):
        res = self.client().delete('/customers/{}'.format(self.customer_id), headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.customer_token)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_customer(self):
        res = self.client().delete('/customers/203', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.customer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)







    '''Test get all customers routes'''
    def test_get_events(self):
        res = self.client().get('/events')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['events'])

    def test_404_get_events(self):
        res = self.client().get('/eventsMISSPEL')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_200_post_events(self):
        res = self.client().post('/events', headers = {'Content-Type': 'application/json',
                                 'Authorization': 'Bearer {}'.format(self.events_token)},
                                 json = self.new_event)
        data = json.loads(res.data)
        print('inserted events id', data['id'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_noBEARRER_post_events(self):
        res = self.client().post('/events', headers = {'Content-Type': 'application/json',
                                 'Authorization': '{}'.format(self.events_token)},
                                 json = self.new_event)
        data = json.loads(res.data)
        self.assertEqual(data['code'], 'invalid_header')

    def test_200_edit_events(self):
        res = self.client().patch('/events/1', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.events_token)},
                                    json = {'event_name': 'EDITED NAME', 'rating': 0000})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_edit_events(self):
        res = self.client().patch('/events/1', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.events_token)},
                                    json = {'MISSPEL_name': 'EDITED NAME', 'rating': 'WRONG DATA'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_200_delete_events(self):
        res = self.client().delete('/events/{}'.format(self.event_id), headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.events_token)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_events(self):
        res = self.client().delete('/events/203', headers = {'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(self.events_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


if __name__ == '__main__':
    unittest.main()
