__author__ = 'fki'

import json
import pandas as p
import pandas.tseries.offsets as offsets
import voluptuous as v
from collections import OrderedDict
from django.core.exceptions import ValidationError
from apps.referencepool.models import Individual, DataClass
import logging
log = logging.getLogger(__name__)

class TimeResolutions(object):

    YEAR = 'year'
    QUARTER = 'quarter'
    MONTH = 'month'
    DAY = 'day'

    SUPPORT = {
        DAY: {
            'level': 10,
            'display_name': 'Day',
        },
        MONTH: {
            'level': 20,
            'display_name': 'Month',
        },
        QUARTER: {
            'level': 30,
            'display_name': 'Quarter',
        },
        YEAR: {
            'level': 40,
            'display_name': 'Year',
        }
    }

    @staticmethod
    def is_supported(value):
        if value in TimeResolutions.SUPPORT:
            return True
        else:
            return False


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
    def from_json(data, params):
        obj = json.loads(data, object_pairs_hook=OrderedDict)

        rng = p.date_range('2011-01-01', '2012-02-01', freq=offsets.MonthBegin())

        rng.get_values()
        log.info(rng.get_values())

        ts = p.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], index=rng)
        converted = ts.resample(offsets.YearBegin(), how='mean')
        log.info(converted)

        return DatasetData(data=obj)

    def validate(self, time_start, time_end, class_id):

        def validate_individual(value):
            if class_id != 7:
                if not isinstance(value, int):
                    raise v.Invalid("Individual of Element %d of data.table is not an integer."
                                     " Please use class 'custom' to provide strings.")

        if not isinstance(self.data, dict):
            raise ValidationError("Data field needs to be a dictionary.")

        schema = v.Schema({
            v.Required('table', msg="Data dict needs a 'table' field."): v.All([
                {
                    v.Required('row'): int,
                    v.Required('individual'): validate_individual,
                    v.Required('values'): v.All(
                        dict
                    ),
                }
            ], v.Length(min=1))
        })

        try:
            schema(self.data)
        except v.Invalid as e:
            raise ValidationError(e)

        raise ValidationError("hallo")

        #
        #     # ToDo Validate time range
        #     row = value['values']





