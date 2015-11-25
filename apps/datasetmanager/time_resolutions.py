import abc
import datetime
from pandas import offsets

__author__ = 'fki'


class TimeResolutionBase(metaclass=abc.ABCMeta):
    """
    A base class for creating time resolutions
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        return

    @property
    @abc.abstractmethod
    def display_name(self) -> str:
        return

    @property
    @abc.abstractmethod
    def level(self) -> int:
        return

    @property
    @abc.abstractmethod
    def offset(self) -> offsets.DateOffset:
        return

    @abc.abstractmethod
    def input_expr(self, date: str) -> datetime.date:
        return

    @abc.abstractmethod
    def output_expr(self, date: datetime.date) -> str:
        return


class Day(TimeResolutionBase):
    @property
    def name(self):
        return "day"

    @property
    def display_name(self):
        return "Day"

    def input_expr(self, date):
        return '%s' % date

    def output_expr(self, date):
        return date.strftime('%Y-%m-%d')

    @property
    def level(self):
        return 10

    @property
    def offset(self):
        return offsets.Day()


class Month(TimeResolutionBase):
    @property
    def name(self):
        return "month"

    @property
    def display_name(self):
        return "Month"

    def input_expr(self, date):
        return '%s-01' % date

    def output_expr(self, date):
        return date.strftime('%Y-%m')

    @property
    def level(self):
        return 20

    @property
    def offset(self):
        return offsets.MonthBegin()


class Quarter(TimeResolutionBase):
    @property
    def name(self):
        return "quarter"

    @property
    def display_name(self):
        return "Quarter"

    def input_expr(self, date):
        date = date.split("-")
        if date[1] == 'Q1':
            return '%s-01-01' % date[0]
        if date[1] == 'Q2':
            return '%s-04-01' % date[0]
        if date[1] == 'Q3':
            return '%s-07-01' % date[0]
        if date[1] == 'Q4':
            return '%s-10-01' % date[0]

    def output_expr(self, date: datetime.date):
        if date.month == 1:
            return date.strftime('%Y-Q1')
        if date.month == 4:
            return date.strftime('%Y-Q2')
        if date.month == 7:
            return date.strftime('%Y-Q3')
        if date.month == 10:
            return date.strftime('%Y-Q4')

    @property
    def level(self):
        return 30

    @property
    def offset(self):
        return offsets.QuarterBegin(startingMonth=1)


class Year(TimeResolutionBase):
    @property
    def name(self):
        return "year"

    @property
    def display_name(self):
        return "Year"

    def input_expr(self, date):
        return '%s-01-01' % date

    def output_expr(self, date):
        return date.strftime('%Y')

    @property
    def level(self):
        return 40

    @property
    def offset(self):
        return offsets.YearBegin()


class TimeResolutions(object):
    """
    Manages all available time resolution objects
    """

    def __init__(self):
        self.resolutions = [
            Day(),
            Month(),
            Quarter(),
            Year()
        ]

    def get(self, value: str) -> TimeResolutionBase:
        for r in self.resolutions:
            if r.name == value:
                return r
        return None

    def is_supported(self, value: str):
        for r in self.resolutions:
            if r.name == value:
                return True
        return False

    def get_supported_names(self):
        return [r.name for r in self.resolutions]
