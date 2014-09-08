"""
Unittests for the pandas DataFrame adapter
"""

import logging as log


from django.test import TestCase
import datetime
from ..metricdata import MetricData


class MetricDataTest(TestCase):

    def test_sort_metric_data(self):

        base_data = [
            {'value': 23900.0, 'from_date': datetime.date(2004, 1, 1), 'row': 1, 'id': 1, 'to_date': datetime.date(2004, 12, 31), 'metric_id': 1},
            {'value': 22232.0, 'from_date': datetime.date(2005, 1, 1), 'row': 2, 'id': 2, 'to_date': datetime.date(2005, 12, 31), 'metric_id': 1},
            {'value': 13443.0, 'from_date': datetime.date(2004, 1, 1), 'row': 3, 'id': 3, 'to_date': datetime.date(2004, 12, 31), 'metric_id': 1},
            {'value': 16534.0, 'from_date': datetime.date(2005, 1, 1), 'row': 4, 'id': 4, 'to_date': datetime.date(2005, 12, 31), 'metric_id': 1},
            {'value': 23242.0, 'from_date': datetime.date(2004, 1, 1), 'row': 5, 'id': 5, 'to_date': datetime.date(2004, 12, 31), 'metric_id': 1},
            {'value': 12233.0, 'from_date': datetime.date(2005, 1, 1), 'row': 6, 'id': 6, 'to_date': datetime.date(2005, 12, 31), 'metric_id': 1},
            {'value': 34423.0, 'from_date': datetime.date(2004, 1, 1), 'row': 7, 'id': 7, 'to_date': datetime.date(2004, 12, 31), 'metric_id': 1},
            {'value': 21223.0, 'from_date': datetime.date(2005, 1, 1), 'row': 8, 'id': 8, 'to_date': datetime.date(2005, 12, 31), 'metric_id': 1}
        ]

        column1 = ['Germany', 'Germany', 'Germany', 'Germany', 'Spain', 'Spain', 'Spain', 'Spain']
        column2 = ['25', '25', '35', '35', '25', '25', '35', '35']

        df = MetricData(base_data)
        df.add_column('Country', column1)
        df.add_column('Age Class', column2)

        columns = df.get_column_values('Country')
        dataframe = df.get_df()

        self.assertTrue("Germany" in columns)
        self.assertTrue("Spain" in columns)
        self.assertTrue("Country" in dataframe.columns.values)
        self.assertTrue("Age Class" in dataframe.columns.values)
        self.assertEqual(len(dataframe.index), 8)
        self.assertEqual(dataframe['value'][0], "23900.0")

        df.sort_by(['value'])
        dataframe = df.get_df()

        self.assertEqual(dataframe['value'].values[0], "12233.0")
        self.assertEqual(dataframe['value'].values[7], "34423.0")


    def test_filter_metric_data(self):

        base_data = [
            {'value': 23900.0, 'from_date': datetime.date(2004, 1, 1), 'row': 1, 'id': 1, 'to_date': datetime.date(2004, 12, 31), 'metric_id': 1},
            {'value': 22232.0, 'from_date': datetime.date(2005, 1, 1), 'row': 2, 'id': 2, 'to_date': datetime.date(2005, 12, 31), 'metric_id': 1},
            {'value': 13443.0, 'from_date': datetime.date(2004, 1, 1), 'row': 3, 'id': 3, 'to_date': datetime.date(2004, 12, 31), 'metric_id': 1},
            {'value': 16534.0, 'from_date': datetime.date(2005, 1, 1), 'row': 4, 'id': 4, 'to_date': datetime.date(2005, 12, 31), 'metric_id': 1},
            {'value': 23242.0, 'from_date': datetime.date(2004, 1, 1), 'row': 5, 'id': 5, 'to_date': datetime.date(2004, 12, 31), 'metric_id': 1},
            {'value': 12233.0, 'from_date': datetime.date(2005, 1, 1), 'row': 6, 'id': 6, 'to_date': datetime.date(2005, 12, 31), 'metric_id': 1},
            {'value': 34423.0, 'from_date': datetime.date(2004, 1, 1), 'row': 7, 'id': 7, 'to_date': datetime.date(2004, 12, 31), 'metric_id': 1},
            {'value': 21223.0, 'from_date': datetime.date(2005, 1, 1), 'row': 8, 'id': 8, 'to_date': datetime.date(2005, 12, 31), 'metric_id': 1}
        ]

        column1 = ['Germany', 'Germany', 'Germany', 'Germany', 'Spain', 'Spain', 'Spain', 'Spain']
        column2 = ['25', '25', '35', '35', '25', '25', '35', '35']

        df = MetricData(base_data)
        df.add_column('Country', column1)
        df.add_column('Age Class', column2)

        df.where({
            'Country': ['Germany','Spain'],
            'value': ['23242.0']
        })
        dataframe = df.get_df()

        self.assertEqual(len(dataframe.index), 1)
        self.assertEqual(dataframe['row'].values[0], "5")
        self.assertEqual(1, 1, "The number is not bigger")
