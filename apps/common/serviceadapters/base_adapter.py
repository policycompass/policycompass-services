import requests

__author__ = 'fki'


class BaseAdapter(object):
    """
    Basis for implementing adapters to simple RESTful service.
    WORK IN PROGRESS: Just GET method is supported for now.
    Derive specific adapters from this class and set the url and url_entity
    properties.

    e.g.
    self.url = 'http://domain"
    self.url_entity = self.url + '/%s'
    """

    url = None
    url_entity = None

    def __init__(self):
        """
        Initialize the url properties.
        """
        if not self.url:
            raise Exception('url Property is not set')
        if not self.url_entity:
            raise Exception('url_entity Property is not set')

    def get(self, id=None):
        """
        Encapsulates the GET method
        """
        # Get one entity
        if id:
            url = self.url_entity % id
            response = requests.get(url)
        # Get the list of the resources
        else:
            response = requests.get(self.url)
        # Return the response as JSON
        return response.json()

    def post(self, data):
        raise NotImplementedError

    def update(self, id, data):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError
