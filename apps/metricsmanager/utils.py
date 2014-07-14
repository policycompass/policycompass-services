__author__ = 'fki'

import datetime
import logging
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from django.db import connection

log = logging.getLogger(__name__)


def get_rawdata_for_metric(metric, extras=True):
    from .models import Metric
    if not type(metric) is Metric:
        raise ValueError('First argument is not a metric model instance')

    result = {}

    raw_data = metric.rawdata_set.all()
    raw_data_extra = metric.rawdataextra_set.select_related('category').all()

    result['extra_columns'] = []

    for e in raw_data_extra:
        result['extra_columns'].append(e.category.title)

    result['table'] = []

    for r in raw_data:

        item = {
            'row': r.row,
            'value': r.value,
            'from': r.from_date,
            'to': r.to_date
        }

        for e in raw_data_extra:
            ident = e.category.title
            try:
                extra = e.rawdataextradata_set.get(raw_data_extra=e, row=r.row)
                item[ident] = extra.value
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                log.error("Integrity Error with Raw Data Extra Data")

        result['table'].append(item)

    return result

def save_rawdata_for_metric(metric, value):
    from .models import RawData, RawDataExtra, RawDataExtraData, RawDataCategory
    log.info(value)
    row_number = 1

    extra_mapping = {}

    for e in value['extra_columns']:
        raw_data_category = RawDataCategory.objects.get(title=e)
        raw_data_extra = RawDataExtra()
        raw_data_extra.metric = metric
        raw_data_extra.category = raw_data_category
        raw_data_extra.save()
        extra_mapping[e] = raw_data_extra

    for r in value['table']:
        raw = RawData()

        raw.metric = metric
        raw.from_date = r['from']
        raw.to_date = r['to']
        raw.row = row_number
        raw.value = r['value']
        raw.save()

        for e in value['extra_columns']:
            raw_extra = RawDataExtraData()
            raw_extra.row = row_number
            raw_extra.value = r[e]
            raw_extra.raw_data_extra = extra_mapping[e]
            raw_extra.save()

        row_number += 1



