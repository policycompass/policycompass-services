from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from apps.referencepool.models import *
import requests
import json
import os

__author__ = 'fki'


class Command(BaseCommand):
    help = 'Harvest external resources to fill the Reference Pool'

    def handle(self, *args, **options):
        if args:
            for a in args:
                try:
                    func = getattr(self, '_harvest_' + a)
                except AttributeError:
                    self.stdout.write('No such Harvester')
                func()
        else:
            self.stdout.write('Harvesting everything')
            for f in dir(self):
                if f.startswith('_harvest_'):
                    getattr(self, f)()

    def _harvest_languages(self):
        self.stdout.write('Harvesting Languages')
        url = 'http://data.okfn.org/data/core/language-codes/r/language-codes.json'
        result = json.loads((requests.get(url)).text)
        for lang in result:
            try:
                l = Language(code=lang['alpha2'], title=lang['English'])
                l.save()
            except IntegrityError:
                pass
        self.stdout.write('Successfully Harvested Languages')

    def _harvest_countries(self):
        self.stdout.write('Harvesting Countries')
        url = 'http://data.okfn.org/data/core/country-codes/r/country-codes.json'
        result = json.loads((requests.get(url)).text)
        country_class = DataClass.objects.get(title='Country')

        for country in result:
            try:
                c = Individual(data_class=country_class, title=country['name'],
                               code=country['ISO3166-1-Alpha-3'])
                c.save()
            except IntegrityError:
                pass

    def _harvest_external_resources(self):
        self.stdout.write('Harvesting External Resources')
        result = self._file_to_json('../../resources/open-data-monitor.json')
        for resource in result:
            try:
                name = result[resource]['col_1'].replace('_', '.').replace('-',
                                                                           '.')
                url = 'http://' + name
                r = ExternalResource(title=name, url=url, api_url=url)
                r.save()
            except IntegrityError:
                pass

    def _file_to_json(self, rel_path):
        dir = os.path.dirname(__file__)
        abs_path = os.path.join(dir, rel_path)
        with open(abs_path, "r") as file:
            data = json.load(file)
        return data
