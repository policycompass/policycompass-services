__author__ = 'fki'

import requests


class BaseAdapter(object):

    url = None
    url_entity = None

    def __init__(self):
        if not self.url:
            raise Exception('url Property is not set')
        if not self.url_entity:
            raise Exception('url_entity Property is not set')

    def get(self, id=None):
        if id:
            url = self.url_entity % id
            response = requests.get(url)
        else:
            response = requests.get(self.url)
        return response.json()

        pass

    def post(self, data):
        raise NotImplementedError

    def update(self, id, data):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError