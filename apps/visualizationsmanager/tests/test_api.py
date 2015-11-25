from rest_framework import status
from rest_framework.test import APITestCase


class ApiTests(APITestCase):
    # Load the test data
    fixtures = ['visualisation.json']

    def setUp(self):
        self.url_base = '/api/v1'

    def build_url(self, url):
        return self.url_base + url

    def test_get_visualizations(self):
        response = self.client.get(self.build_url('/visualizations'))
        self.assertEqual(len(response.data), 2)

    def test_get_visualizations2(self):
        response = self.client.get(self.build_url('/visualizations/1'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '{"id": 1, '
                                           '"title": "Test Visualizations", '
                                           '"description": "This is a first test visualizations.", '
                                           '"issued": "2014-05-03T00:00:00Z"}')

    def test_post_visualizations(self):
        data = {"title": "Third Test Visualizations",
                "description": "This is a third visualizations.",
                "issued": "2014-05-15T00:00:00Z"}

        response = self.client.post(self.build_url('/visualizations'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.get(self.build_url('/visualizations/3'))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
