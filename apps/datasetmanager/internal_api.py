from apps.datasetmanager.models import Dataset
from apps.datasetmanager.dataset_data import DatasetData

""" Internal API for datasetmanager for basic opeerations.

The internal api for the datasetmanager supports basic CRDU-like function for datasets. It requires
no knowledge about the marshalling of the dataset models and is just a thin wrapper arround the
provided models.

Currently it does not handle creation of datasets, for thos the models should be used directly.
"""

""" Get a dataset by its id. """
def get(dataset_id: int):
    dataset = Dataset.objects.get(pk=dataset_id)
    dataset.data = DatasetData.from_json(dataset.data)
    return dataset

""" Get all datasets matching filter.

Gets all dataset which fields match the provided kwargs. This might result in a table scan if no
index exists for the given field.
"""
def filter(**kwargs):
    datasets = Dataset.objects.filter(**kwargs)
    for dataset in datasets:
        dataset.data = DatasetData.from_json(dataset.data)
    return datasets

"""Store a data set.

Store a fully populated dataset object. This currently requires a lot of internal knwoledge about
the model. It should rather work with kwargs as well instead.
"""
def store(dataset):
    dataset.data = dataset.data.get_json()
    dataset.save()
    return dataset.id
