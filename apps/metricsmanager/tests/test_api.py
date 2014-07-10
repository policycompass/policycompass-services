import logging as log

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import unittest

class ApiTests(APITestCase):

    # Load the test data
    fixtures = ['metrics.json']

    def setUp(self):
        self.url_base = '/api/v1'

    def build_url(self, url):
        return self.url_base + url

    def test_get_metrics(self):
        response = self.client.get(self.build_url('/metrics'))
        self.assertEqual(len(response.data), 2)

    def test_get_metric(self):
        response = self.client.get(self.build_url('/metrics/1'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '{"id": 1, '
                                           '"title": "Test Metric", '
                                           '"description": "This is a first test metric.", '
                                           '"issued": "2014-05-03T00:00:00Z"}')

    def test_post_metric(self):
        data = {"title": "Third Test Metric",
                "description": "This is a third metric.",
                "issued": "2014-05-15T00:00:00Z"}

        response = self.client.post(self.build_url('/metrics'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.get(self.build_url('/metrics/3'))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)






