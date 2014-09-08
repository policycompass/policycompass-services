"""
Encapsulates methods of the pandas DataFrame to match the Metrics Managers requirements
"""
__author__ = 'fki'

import logging
from pandas import DataFrame

log = logging.getLogger(__name__)


class MetricData(object):
    """
    Encapsulates methods of the pandas DataFrame to match the Metrics Managers requirements.
    The sort and where operations can be chained.
    """

    def __init__(self, dict):
        """
        Initializes the DataFrame.
        The dict parameter has to be list of dictionaries, where each dict represents a row of the table.
        """
        self.df = DataFrame(dict)
        # Convert every cell to string
        self.df = self.df.astype(str)

    def add_column(self, name, column):
        """
        Adds a new column to the DataFrame.
        The column has to be list with the same dimension as the initial data.
        """
        self.df[name] = column
        self.df = self.df.astype(str)
        return self.df

    def get_column_values(self, column):
        """
        Returns the ranges of a given column.
        """
        return self.df[column].unique().tolist()

    def sort_by(self, sort, order=None):
        """
        Sorts the data frame by columns.
        sort: The column(s) as list - e.g.  ['column1', 'column2']
        order: The order of the sorting: asc or desc
        """
        ascending = True
        if order == 'desc':
            ascending = False

        self.df = self.df.sort(sort, ascending=ascending)
        return self

    def where(self, value):
        """
        Filters the DataFrame by given values for specific columns
        value: A dictionary of lists.
         e.g {
            'Country': ['Germany','Spain'],
            'value': ['23242.0']
        }
        """
        index = True

        for filter, value in value.items():
            index_value = False
            for f in value:
                # OR conjunction for the values of the filter
                index_value = index_value | (self.df[filter] == f)

            # AND conjunction for all filters
            index = index & index_value

        self.df = self.df[index]
        return self

    def get_df(self):
        """
        Returns the DataFrame object
        """
        return self.df



