import os
from unittest import TestCase
from urllib.parse import urlparse, parse_qs
from infusionsoft.client import Client


class InfusionsoftTestCases(TestCase):

    def setUp(self):
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.token = os.environ.get('ACCESS_TOKEN')
        self.redirect_url = os.environ.get('REDIRECT_URL')
        self.client = Client(client_id=self.client_id, client_secret=self.client_secret, token=self.token)

    def test_oauth_access(self):
        url = self.client.oauth_access(self.redirect_url)
        self.assertIsInstance(url, str)
        o = urlparse(url)
        query = parse_qs(o.query)
        self.assertIn('client_id', query)
        self.assertEqual(query['client_id'][0], self.client_id)
        self.assertIn('redirect_uri', query)
        self.assertEqual(query['redirect_uri'][0], self.redirect_url)

    def test_get_data(self):
        response = self.client.get_data(endpoint="contacts", order="id", order_direction="descending", limit=1)
        self.assertIsInstance(response, dict)

    def test_create_data(self):
        data = {'email_addresses': [{'email': 'EMAIL@EMAIL.com', 'field': 'EMAIL1'}], 'given_name': 'MYNAME'}
        response = self.client.create_data("contacts", **data)
        print(response)
        self.assertIsInstance(response, bool)