__author__ = 'fki'

import datetime
import logging
log = logging.getLogger(__name__)


def get_rawdata_for_metric(metric, extras=True):
    from .models import Metric
    if not type(metric) is Metric:
        raise ValueError('First argument is not a metric model instance')

    result = {}
    raw_data = metric.rawdata_set.all()

    result['value'] = []
    result['from'] = []
    result['to'] = []

    for r in raw_data:
        result['value'].append(r.value)
        result['from'].append(r.from_date)
        result['to'].append(r.to_date)

    raw_data_extra = metric.rawdataextra_set.all()

    if extras:
        result['extras'] = {}
        for r in raw_data_extra:
            ident = r.category.title
            result['extras'][ident] = []
            extra_data = r.rawdataextradata_set.all()

            for d in extra_data:
                result['extras'][ident].append(d.value)

    return result

def save_rawdata_for_metric(metric, value):
    from .models import RawData

    log.info(value)

    l = len(value['value'])
    for i in range(0, l):
        raw = RawData()
        raw.metric = metric
        raw.from_date = value['from'][i]
        raw.to_date = value['to'][i]
        raw.row = i + 1
        raw.value = value['value'][i]
        raw.save()
