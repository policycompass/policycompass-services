__author__ = 'fki'

import logging
from pandas import DataFrame

log = logging.getLogger(__name__)


class MetricData(object):


    def __init__(self, dict):
        self.df = DataFrame(dict)
        self.df = self.df.astype(str)

    def add_column(self, name, column):
        self.df[name] = column
        self.df = self.df.astype(str)
        return self.df

    def get_column_values(self, column):
        return self.df[column].unique().tolist()

    def sort_by(self, sort, order=None):
        ascending = True
        if order == 'desc':
            ascending = False

        self.df = self.df.sort(sort, ascending=ascending)
        return self

    def where(self, value):
        index = True

        for filter, value in value.items():
            index_value = False
            for f in value:
                index_value = index_value | (self.df[filter] == f)

            index = index & index_value

        self.df = self.df[index]

        return self

    def get_df(self):
        return self.df



