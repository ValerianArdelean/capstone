import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Providers, Customers, setup_db


class TestProviders(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        print('setupclass')

    @classmethod
    def tearDownClass(cls):
        print('teardownclass')

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://localhost:5432/test_db'
        setup_db(self.app)

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

    '''Test get for a provider'''
    def test_200_get_provider(self):
        res = self.client().get('/providers/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_provider(self):
        pass

    def test_edit_provider(self):
        pass

    def test_delete_provider(self):
        pass







    def test_get_customers(self):
        res = self.client().get('/customers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cityes'])

    def test_search_customers(self):
        pass

    def test_post_customers(self):
        pass

    def test_get_customer(self):
        pass

    def test_edit_customer(self):
        pass

    def test_delete_customer(self):
        pass








    def test_get_events(self):
        res = self.client().get('/events')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['events'])

    def test_post_events(self):
        pass

    def test_edit_events(self):
        pass

    def test_delete_events(self):
        pass




if __name__ == '__main__':
    unittest.main()
