__author__ = 'fki'
import os
import csv
import codecs

import logging
log = logging.getLogger(__name__)


class FileEncoder(object):

    supported_extensions = {
        '.csv': '_csv_encode'
    }

    # file: InMemoryUploadedFile
    def __init__(self, file):
        self.file = file
        self.file_name, self.file_ext = os.path.splitext(file.name)

    def is_supported(self):
        if self.file_ext in self.supported_extensions:
            return True
        else:
            return False

    def encode(self):
        result = getattr(self, self.supported_extensions[self.file_ext])()
        return result

    def _csv_encode(self):
        r = []
        reader = csv.reader(codecs.iterdecode(self.file, "utf-8"))
        for row in reader:
            log.info(str(row))
            r.append(row)
        return r
