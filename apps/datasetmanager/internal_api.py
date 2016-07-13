from apps.datasetmanager.models import Dataset
from apps.datasetmanager.dataset_data import DatasetData


def get(dataset_id: int):
    """ Internal API for datasetmanager for basic opeerations.

    The internal api for the datasetmanager supports basic CRDU-like function
    for datasets. It requires no knowledge about the marshalling of the dataset
     models and is just a thin wrapper arround the
    provided models.

    Currently it does not handle creation of datasets, for thos the models
    should be used directly.
    """
    """ Get a dataset by its id. """
    dataset = Dataset.objects.get(pk=dataset_id)
    dataset.data = DatasetData.from_json(dataset.data)
    return dataset


def filter(**kwargs):
    """ Get all datasets matching filter.

    Gets all dataset which fields match the provided kwargs. This might result
    in a table scan if no
    index exists for the given field.
    """
    datasets = Dataset.objects.filter(**kwargs)
    for dataset in datasets:
        dataset.data = DatasetData.from_json(dataset.data)
    return datasets


def store(dataset):
    """Store a data set.
    Store a fully populated dataset object. This currently requires a lot of
    internal knwoledge about  the model. It should rather work with kwargs as
    well instead.
    """
    dataset.data = dataset.data.get_json()
    dataset.save()
    return dataset.id


def remove_metric_link(metric_id):
    """Removes Link to Metric from all Datasets that are linked to a given metric.
    Is called by post_delete signal in metric.
    """
    datasets = Dataset.objects.filter(metric_id=metric_id)
    for dataset in datasets:
        dataset.metric_id = None
        dataset.description = ''
        dataset.save()
