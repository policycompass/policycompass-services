__author__ = 'fki'

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from apps.referencepool.models import *
import requests, json


class Command(BaseCommand):
    help = 'Harvest external resources to fill the Reference Pool'

    def handle(self, *args, **options):
        self._harvest_languages()

        self.stdout.write('Successfully closed poll')

    def _harvest_languages(self):
        url = 'http://data.okfn.org/data/core/language-codes/r/language-codes.json'
        result = json.loads((requests.get(url)).text)
        for lang in result:
            try:
                l = Language(code=lang['alpha2'], title=lang['English'])
                l.save()
            except IntegrityError:
                pass