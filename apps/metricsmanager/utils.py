"""
Utility module for retrieving and saving the raw data of metric.
This is functionality of the Metric model, but put here to improve readability.
"""

__author__ = 'fki'

import logging
from .metricdata import MetricData
from collections import OrderedDict

log = logging.getLogger(__name__)


def get_rawdata_for_metric(metric, sort=None, order=None, filter=None):
    """
    Getting the raw data for a given metric.
    metric: Instance of a metric model
    """
    from .models import Metric, RawDataExtraData
    # Its has to be a metric model
    if not type(metric) is Metric:
        raise ValueError('First argument is not a metric model instance')

    result = {}

    # Getting the basic raw data
    raw_data = metric.rawdata_set.all()

    # Creating the data structure with the basic columns
    data = MetricData(list(raw_data.values()))

    # Getting the extra columns
    raw_data_extra = metric.rawdataextra_set.select_related('category', 'raw_data_extra')
    # Getting the data for the extra columns

    result['extra_columns'] = []

    for e in raw_data_extra:
        # Save the title of the extra columns
        result['extra_columns'].append(e.category.title)
        # Adding the extra column data to the data structure
        raw_ed = RawDataExtraData.objects.filter(raw_data_extra=e)
        data.add_column(e.category.title, raw_ed.values_list('value', flat=True))
        #log.info(raw_ed.values_list('value', flat=True))

    result['table'] = []

    # Pass the query parameter to the MetricData object
    if filter:
        data.where(filter)

    if sort:
        data.sort_by(sort,order)

    # Creating the ranges attribute.
    result['ranges'] = {}
    for e in result['extra_columns']:
        result['ranges'][e] = data.get_column_values(e)

    # Building the result
    items = data.get_df()
    row = 1
    # Iterate over the DataFrame
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
    """
    Saves new raw data for a given metric.
    metric: Instance of a metric model
    value: data structure according the raw data data structure
    """
    from .models import RawData, RawDataExtra, RawDataExtraData, RawDataCategory
    log.info(value)
    row_number = 1

    extra_mapping = {}

    # Save the available extra columns
    for e in value['extra_columns']:
        raw_data_category = RawDataCategory.objects.get(title=e)
        raw_data_extra = RawDataExtra()
        raw_data_extra.metric = metric
        raw_data_extra.category = raw_data_category
        raw_data_extra.save()
        # Hold to the model objects for later use
        extra_mapping[e] = raw_data_extra

    # Save the table data
    for r in value['table']:
        raw = RawData()

        raw.metric = metric
        raw.from_date = r['from']
        raw.to_date = r['to']
        raw.row = row_number
        raw.value = r['value']
        raw.save()

        # Save the extra column values
        for e in value['extra_columns']:
            raw_extra = RawDataExtraData()
            raw_extra.row = row_number
            raw_extra.value = r[e]
            # Reuse the extra column object to create the relation
            raw_extra.raw_data_extra = extra_mapping[e]
            raw_extra.save()

        row_number += 1

def update_rawdata_for_metric(metric, value):
    """
    Updates raw data of metric.
    metric: Instance of a metric model
    value: data structure according the raw data data structure
    """
    from .models import Metric
    if not type(metric) is Metric:
        raise ValueError('First argument is not a metric model instance')

    # Delete all old raw data
    raw_data = metric.rawdata_set.all()
    raw_data.delete()
    raw_data_extra = metric.rawdataextra_set.all()
    raw_data_extra.delete()

    # Save the new raw data
    save_rawdata_for_metric(metric, value)



