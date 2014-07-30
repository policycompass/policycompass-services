__author__ = 'fki'

import datetime
import logging
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from django.db import connection

log = logging.getLogger(__name__)


def get_rawdata_for_metric(metric, extras=True):
    from .models import Metric, RawDataExtraData
    if not type(metric) is Metric:
        raise ValueError('First argument is not a metric model instance')

    result = {}

    raw_data = metric.rawdata_set.all()
    raw_data_extra = metric.rawdataextra_set.select_related('category', 'raw_data_extra')

    raw_data_extra_data = RawDataExtraData.objects.filter(raw_data_extra=raw_data_extra)

    result['extra_columns'] = []
    column_mapping = {}

    for e in raw_data_extra:
        result['extra_columns'].append(e.category.title)
        column_mapping[e.id] = e.category.title
    result['table'] = []

    extra_data = {}
    for ed in raw_data_extra_data:
        r = ed.row
        if r in extra_data:
            extra_data[r][column_mapping[ed.raw_data_extra_id]] = ed.value
        else:
            extra_data[r] = {
                column_mapping[ed.raw_data_extra_id]: ed.value
            }

    #log.info(extra_data)
    for r in raw_data:
        #log.info("HALLLO")
        item = {
            'row': r.row,
            'value': r.value,
            'from': r.from_date,
            'to': r.to_date
        }

        item.update(extra_data[r.row])
        #
        # for e in raw_data_extra:
        #     ident = e.category.title
        #     try:
        #         extra = raw_data_extra_data.filter(row=r.row,raw_data_extra=e)
        #         item[ident] = extra[0].value
        #     except (ObjectDoesNotExist, MultipleObjectsReturned):
        #         log.error("Integrity Error with Raw Data Extra Data")

        result['table'].append(item)

    log.info(connection.queries)
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



