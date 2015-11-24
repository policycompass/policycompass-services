from apps.datasetmanager.models import Dataset

"""Predefined normalisers for use in formulas.

A normaliser is a function which takes all values of a data set and mapps to into the [0,1]
interval. They are use to combine otherwise incompatible metrics.
"""


def get_normalizers():
    normalizers = [
        LinearBoundsNormalizer()
    ]
    return {normalizer.acronym: normalizer for normalizer in normalizers}


class LinearBoundsNormalizer():
    """ Normalize data set by distributing linear between upper and lower bound.

    1      __
          /
         /
    0 __/

      --l--u--->
    """

    acronym = "norm"
    name = "Linear bounds normalizers"
    description = "Maps all smaller than the lower bound to zero and all " \
                  "bigger than upper bound to one. In between values are " \
                  "distributed linearly"

    def __call__(self, dataset: Dataset, lower_bound: int, upper_bound: int):
        return dataset.applymap(lambda x: min(1, max(0, (x - lower_bound) / (upper_bound - lower_bound))))

    def get_arguments(self):
        """ Get arguments that can be used in the formula. """
        return [{"name": "indicator", "type": "indicator"},
                {"name": "lower bound", "type": "int"},
                {"name": "upper bound", "type": "int"}]
