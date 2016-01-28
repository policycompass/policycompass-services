import json
import pandas as p
import numpy
import voluptuous as v
from collections import OrderedDict
from django.core.exceptions import ValidationError
from apps.referencepool.models import Individual, DataClass
from rest_framework import exceptions
from .time_resolutions import TimeResolutions
import logging

log = logging.getLogger(__name__)

__author__ = 'fki'

trl = TimeResolutions()


class TransformationException(exceptions.APIException):
    status_code = 400


class DatasetData(object):
    """
    Wraps the pandas DataFrame to hold the tabular data
    of a dataset. Offers several transformation methods.
    """
    def __init__(self, data_frame: p.DataFrame, unit: int, resolution: str):
        self.unit = unit
        self.resolution = resolution
        self.df = data_frame
        self.time_transformed = False
        self.time_filtered = False
        self.unit_transformed = False

    def get_json(self) -> str:
        """
        Get the data as JSON string
        """
        result = {
            'unit': self.unit,
            'resolution': self.resolution,
            'data_frame': self.df.to_json(date_format='iso')
        }
        return json.dumps(result)

    @staticmethod
    def from_json(data: str):
        """
        Create a DatasetObject from a JSON string
        """
        obj = json.loads(data)
        h = p.read_json(obj['data_frame'])
        h.sort_index(inplace=True)
        dataset_data = DatasetData(h, obj['unit'], obj['resolution'])
        return dataset_data

    def transform_time(self, time_resolution: str):
        """
        Transforms the time series into another valid
        resolution
        """
        if not trl.is_supported(time_resolution):
            raise TransformationException(
                "Time Resolution not supported. Options: " + str(
                    trl.get_supported_names()))

        time_obj = trl.get(time_resolution)
        orig_time_obj = trl.get(self.resolution)

        if time_obj.level < orig_time_obj.level:
            raise TransformationException(
                "Upscaling of the time resolution is not supported.")

        if time_obj != orig_time_obj:
            self.df = self.df.resample(time_obj.offset, how='mean')
            self.resolution = time_obj.name
            self.time_transformed = True

    def filter_by_time(self, start_time: str, end_time: str):
        """
        Filters the data by the given time interval.
        """

        real_start_time = self.get_time_start()
        real_end_time = self.get_time_end()

        if end_time and end_time < real_start_time:
            raise TransformationException(
                "The given end time is less than the start time"
            )

        if start_time and start_time > real_end_time:
            raise TransformationException(
                "The given start time is greater than the end time"
            )

        if start_time and end_time:
            if start_time > end_time:
                raise TransformationException(
                    "The start time cannot be greater than the end time."
                )

        try:
            self.df = self.df.ix[start_time:end_time]
            self.time_filtered = True
        except p.datetools.DateParseError:
            raise TransformationException(
                "The time parameters are malformed. "
                "Please provide a valid date string"
            )

    def filter_by_individuals(self, individuals: list):
        """
        Filters the dataframe by a given list of individuals.
        Raises an exception when individual is not available.
        """
        available_individuals = self.get_individuals()
        filter_inds = []
        for individual in individuals:
            i = int(individual)
            if i not in available_individuals:
                raise TransformationException(
                    "The selected individuals or not valid.")
            else:
                filter_inds.append(i)

        self.df = self.df[filter_inds]
        log.debug(self.df)

        pass

    def get_individuals(self) -> list:
        """
        Returns all available individuals
        as a list of integers
        """
        result = self.df.columns.values
        return [int(x) for x in result]

    def get_time_start(self) -> str:
        time_obj = trl.get(self.resolution)
        if len(self.df.index) == 1:
            return time_obj.output_expr(self.df.index[0])
        else:
            return time_obj.output_expr(self.df.index[0])

    def get_time_end(self) -> str:
        time_obj = trl.get(self.resolution)
        if len(self.df.index) == 1:
            return time_obj.output_expr(self.df.index[0])
        else:
            return time_obj.output_expr(self.df.index[-1])


class DatasetDataTransformer(object):
    """
    Wraps the transformer conveniently
    """
    @staticmethod
    def from_api(data_dict: dict,
                 time_start: str,
                 time_end: str,
                 time_resolution: str,
                 class_id: int,
                 unit_id: int) -> DatasetData:
        trf = DatasetDataFromAPITransformer(data_dict, time_resolution,
                                            time_start, time_end, class_id,
                                            unit_id)
        return trf.get_dataset_data()

    @staticmethod
    def to_api(dataset_data: DatasetData) -> dict:
        trf = DatasetDataToAPITransformer(dataset_data)
        return trf.get_api_data()


class DatasetDataFromAPITransformer(object):
    """
    Generates a DatasetData Object from the datastructure
    used within the API
    """
    def __init__(self, data: dict, time_resolution: str, time_start: str,
                 time_end: str, class_id: int, unit_id: int):
        self.data = data
        self.time_resolution = time_resolution
        self.time_start = time_start
        self.time_end = time_end
        self.class_id = class_id
        self.unit_id = unit_id
        self._dataset_data = None
        self._create_individuals()
        self._pre_validate()
        self.df = self._transform()
        self._dataset_data = DatasetData(
            self.df,
            self.unit_id,
            self.time_resolution
        )

    def get_dataset_data(self) -> DatasetData:
        """
        Returns the actual DatasetData object
        """
        return self._dataset_data

    def _pre_validate(self):
        """
        Performs a pre-validation if the data
        """
        schema = self._get_validation_schema()

        if not isinstance(self.data, dict):
            raise ValidationError("Data field needs to be a dictionary.")

        try:
            schema(self.data)
        except v.Invalid as e:
            raise ValidationError(e)

    def _get_validation_schema(self) -> v.Schema:
        """
        Defines the validation schema
        """

        def validate_individual(value):
            if self.class_id != 7:
                if not isinstance(value, int):
                    raise v.Invalid(
                        "Individual of Element %d of data.table is not an integer."
                        " Please use class 'custom' to provide strings.")

        schema = v.Schema({
            v.Required('table', msg="Data dict needs a 'table' field."): v.All(
                [
                    {
                        v.Required('row'): int,
                        v.Required('individual'): validate_individual,
                        v.Required('values'): v.All(
                            dict
                        ),
                    }
                ], v.Length(min=1))
        })

        return schema

    def _create_individuals(self):

        table = self.data['table']
        for row in table:
            individual = row['individual']
            if isinstance(individual, str):
                # Does it exist already
                # Todo Make this better
                try:
                    saved_ind = Individual.objects.get(title=individual, data_class=self.class_id)
                    row['individual'] = saved_ind.id
                except Individual.DoesNotExist:
                    ind = Individual(
                        title=individual,
                        data_class=DataClass.objects.get(id=7)
                    )
                    ind.save()
                    row['individual'] = ind.id

    def _transform(self) -> p.DataFrame:
        """
        Returns the transformed data as pandas DataFrame, which
        is needed to init the DatasetData
        """
        if not trl.is_supported(self.time_resolution):
            raise ValidationError(
                "The Specified time_resolution is not supported.")

        time_obj = trl.get(self.time_resolution)
        time_range = self._create_time_range()
        f = p.DataFrame(index=time_range)
        table = self.data['table']
        for row in table:
            values = []
            for time in time_range:
                try:
                    values.append(row['values'][time_obj.output_expr(time)])
                except KeyError:
                    raise ValidationError(
                        "Please provide a value for every date within the range and resolution.")
            f[row['individual']] = values
        return f

    def _create_time_range(self) -> p.DatetimeIndex:
        """
        Creates a time index based on the metadata
        """
        time_obj = trl.get(self.time_resolution)
        start = time_obj.input_expr(self.time_start)
        end = time_obj.input_expr(self.time_end)
        return p.date_range(start, end, freq=time_obj.offset)


class DatasetDataToAPITransformer(object):
    """
    Generates the API datastructure from a DatasetData object
    """

    def __init__(self, dataset_data: DatasetData):
        self._dataset_data = dataset_data
        self._view_data = self._transform()

    def get_api_data(self) -> dict:
        """
        Returns the actual dict for the view
        """
        result = {
            'table': self._view_data,
            'individuals': self._dataset_data.get_individuals()
        }

        if self._dataset_data.time_transformed:
            result['time_transformation'] = {
                'resolution': self._dataset_data.resolution,
                'start': self._dataset_data.get_time_start(),
                'end': self._dataset_data.get_time_end(),
                'method': 'mean'
            }

        if self._dataset_data.time_filtered:
            result['time_filter'] = {
                'start': self._dataset_data.get_time_start(),
                'end': self._dataset_data.get_time_end(),
            }

        return result

    def _transform(self) -> dict:
        """
        Transforms the DatasetData into a dict
        """
        time_obj = trl.get(self._dataset_data.resolution)
        result = []
        row = 1
        for index, i in self._dataset_data.df.iteritems():
            new_dict = OrderedDict()
            new_dict['row'] = row
            new_dict['individual'] = int(index)
            new_dict['values'] = OrderedDict()
            for index2, j in i.iteritems():
                if numpy.isnan(j):
                    new_dict['values'][time_obj.output_expr(index2)] = None
                else:
                    new_dict['values'][time_obj.output_expr(index2)] = round(j, 2)

            result.append(new_dict)
            row += 1

        return result
