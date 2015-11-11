"""
Converts uploaded files into a tabular data structure
"""
__author__ = 'fki'
import codecs
import csv
import datetime
import logging
import os

from xlrd import open_workbook, XL_CELL_DATE, xldate_as_tuple

log = logging.getLogger(__name__)


class FileEncoder(object):
    """
    Converts uploaded files into a tabular data structure
    """
    # Register supported extensions with a function
    supported_extensions = {
        '.csv': '_csv_encode',
        '.tsv': '_tsv_encode',
        '.xlsx': '_xlsx_encode',
        '.xls': '_xlsx_encode'
    }

    # file: InMemoryUploadedFile
    def __init__(self, file):
        """
        Initialize file and file_name
        """
        self.file = file
        self.file_name, self.file_ext = os.path.splitext(file.name)

    def is_supported(self):
        """
        Check if there is a converter for the extension
        """
        if self.file_ext in self.supported_extensions:
            return True
        else:
            return False

    def encode(self):
        """
        Class the responsible function and encodes the file.
        Returns the result
        """
        result = getattr(self, self.supported_extensions[self.file_ext])()
        return result

    def _csv_encode(self, delimiter=' '):
        """
        Encodes a CSV file.
        """
        r = []
        reader = csv.reader(codecs.iterdecode(self.file, "utf-8"), delimiter=delimiter)
        for row in reader:
            log.debug(str(row))
            r.append(row)
        return r

    def _tsv_encode(self):
        """
        Encodes a CSV file
        :return: array of data rows
        """
        return self._csv_encode(delimiter='\t')

    def _xlsx_encode(self):
        """
        Encodes XLS and XLSX files.
        """
        r = []
        wb = open_workbook(file_contents=self.file.read())
        sheet = wb.sheet_by_index(0)
        for row in range(sheet.nrows):
            values = []
            for col in range(sheet.ncols):
                cell = sheet.cell(row, col)
                # Date cells have to be converted to return as string
                if cell.ctype == XL_CELL_DATE:
                    v = xldate_as_tuple(cell.value, wb.datemode)
                    v = datetime.datetime(*v)
                    v = datetime.date(v.year, v.month, v.day)
                elif isinstance(cell.value, float):
                    if cell.value == int(cell.value):
                        v = int(cell.value)
                    else:
                        v = str(cell.value)
                else:
                    v = str(cell.value)

                values.append(v)
            r.append(values)
        return r
