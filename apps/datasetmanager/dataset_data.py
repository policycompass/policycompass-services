__author__ = 'fki'

import json
from collections import OrderedDict
from django.core.exceptions import ValidationError
from apps.referencepool.models import Individual, DataClass
import logging
log = logging.getLogger(__name__)


class DatasetData(object):

    TABLE = 'table'

    def __init__(self, data=None):
        if data is None:
            self.data = {}
        else:
            self.data = data

    def set_data(self, data):
        self.data = data

    def get_json(self):
        return json.dumps(self.data)

    def create_individuals(self):
        table = self.data[self.TABLE]
        for row in table:
            individual = row['individual']
            if isinstance(individual, str):
                # Does it exist already
                # Todo Make this better
                try:
                    saved_ind = Individual.objects.get(title=individual)
                    row['individual'] = saved_ind.id
                except Individual.DoesNotExist:
                    ind = Individual(
                        title=individual,
                        data_class=DataClass.objects.get(id=7)
                    )
                    ind.save()
                    row['individual'] = ind.id

    @staticmethod
    def from_json(data):
        obj = json.loads(data, object_pairs_hook=OrderedDict)
        return DatasetData(data=obj)

    def validate(self, time_start, time_end, class_id):
        if not isinstance(self.data, dict):
            raise ValidationError("Data field needs to be a dictionary.")

        if self.TABLE not in self.data:
            raise ValidationError("Data dict needs a 'table' field.")

        table = self.data[self.TABLE]

        if not isinstance(table, list):
            raise ValidationError("Data.table needs to be a list.")

        if len(table) == 0:
            raise ValidationError("Data.table cannot be empty.")

        for index, value in enumerate(table):
            if not isinstance(value, dict):
                raise ValidationError("Element %d of data.table is not a dictionary." % index)
            if 'row' not in value:
                raise ValidationError("Element %d of data.table has not 'row' field." % index)
            if 'individual' not in value:
                raise ValidationError("Element %d of data.table has not 'individual' field." % index)
            if class_id != 7:
                if not isinstance(value['individual'], int):
                    raise ValidationError("Individual of Element %d of data.table is not an integer. "
                                          "Please use class 'custom' to provide strings." % index)
            if 'values' not in value:
                raise ValidationError("Element %d of data.table has not 'values' field." % index)
            if not isinstance(value['values'], dict):
                raise ValidationError("Data.table.value in element %d is not a dictionary." % index)

            # ToDo Validate time range
            row = value['values']





