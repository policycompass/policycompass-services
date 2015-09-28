"""Predefined normalisers for use in formulas.

A normaliser is a function which takes all values of a data set and mapps to into the [0,1]
interval. They are use to combine otherwise incompatible metrics.
"""

def get_normalizers():
    return { "norm": LinearBoundsNormalizer() }

class LinearBoundsNormalizer():
    """ Normalize data set by distributing linear between upper and lower bound.

    1      __
          /
         /
    0 __/

      --l--u--->
    """
    def __call__(self, dataset, lower_bound, upper_bound):
        return dataset.applymap(lambda x: min(1, max(0, (x - lower_bound) / (upper_bound - lower_bound))))
