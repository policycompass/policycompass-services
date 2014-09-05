__author__ = 'fki'

import logging
from .metricdata import MetricData
from collections import OrderedDict

log = logging.getLogger(__name__)


def get_rawdata_for_metric(metric, sort=None, order=None, filter=None):
    from .models import Metric, RawDataExtraData
    if not type(metric) is Metric:
        raise ValueError('First argument is not a metric model instance')

    result = {}

    # Getting the basic raw data
    raw_data = metric.rawdata_set.all()

    # Creating the data structure
    data = MetricData(list(raw_data.values()))

    # Getting the extra columns
    raw_data_extra = metric.rawdataextra_set.select_related('category', 'raw_data_extra')
    # Getting the data for the extra columns
    raw_data_extra_data = RawDataExtraData.objects.filter(raw_data_extra=raw_data_extra)

    result['extra_columns'] = []

    for e in raw_data_extra:
        result['extra_columns'].append(e.category.title)
        # Adding the extra column data to the data structure
        raw_ed = RawDataExtraData.objects.filter(raw_data_extra=e)
        data.add_column(e.category.title, raw_ed.values_list('value', flat=True))
        #log.info(raw_ed.values_list('value', flat=True))

    result['table'] = []

    if filter:
        data.where(filter)

    if sort:
        data.sort_by(sort,order)

    result['ranges'] = {}
    for e in result['extra_columns']:
        result['ranges'][e] = data.get_column_values(e)

    items = data.get_df()
    row = 1
    for index, i in items.iterrows():
        item = OrderedDict()
        item['row'] = row
        item['from'] = i['from_date']
        item['to'] = i['to_date']
        item['value'] = i['value']

        for e in result['extra_columns']:
            item[e] = i[e]

        result['table'].append(item)
        row += 1

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

def update_rawdata_for_metric(metric, value):
    from .models import Metric
    if not type(metric) is Metric:
        raise ValueError('First argument is not a metric model instance')

    raw_data = metric.rawdata_set.all()
    raw_data.delete()
    raw_data_extra = metric.rawdataextra_set.all()
    raw_data_extra.delete()

    save_rawdata_for_metric(metric, value)



