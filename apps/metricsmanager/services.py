import itertools
import datetime

from django.core.exceptions import ValidationError

from apps.datasetmanager import internal_api as dataset_api
from apps.datasetmanager.models import Dataset
from apps.datasetmanager.dataset_data import DatasetData

from .formula import compute_formula


def validate_operationalize(data):
    """
    Validate data handed to operationalize.
    """

    # check if dataset with same name exists
    if dataset_api.filter(title=data['title']):
        raise ValidationError({"title": "Dataset name is not unique."})

    # ensure there are datasets
    if 'datasets' not in data:
        raise ValidationError({"datasets": "At least one dataset is required."})

    datasets = {variable: dataset_api.get(dataset_id) for
                (variable, dataset_id) in data['datasets'].items()}

    # ensure all datasets have the same class
    class_id = next(iter(datasets.values())).class_id
    if not all([d.class_id == class_id for d in datasets.values()]):
        raise ValidationError({
            "datasets": "All datasets need to have the same class"
        })

    # ensure all datasets have the same time_resolution
    resolution = next(iter(datasets.values())).data.resolution
    if not all([d.data.resolution == resolution for d in datasets.values()]):
        return ValidationError({
            "datasets": "All datasets need to have the same time resolution"
        })

    results = {}
    results.update(data)
    results.update({
        "class_id": class_id,
        "datasets": datasets,
        "time_resolution": resolution,
    })
    return results


def compute_dataset(formula, datasets, title, unit_id, time_resolution,
                    indicator_id, class_id, creator_path, metric_id=None):
    """
    Compute and store a dataset. Returns the id of the newly created dataset.
    """

    result = compute_formula(formula, datasets)
    data = DatasetData(
        data_frame=result,
        unit=unit_id,
        resolution=time_resolution)

    dataset = Dataset(
        title=title,
        description="Computed formula '%s' with %s" % (
            formula,
            ", ".join(["'%s' as %s" % (title, variable) for
                       variable, dataset in datasets.items()])),
        keywords=", ".join(set(itertools.chain(
            [dataset.keywords for dataset in datasets.values()]))),
        version=0,
        # ressource related info
        resource_url="not available",
        resource_issued=datetime.datetime.now(),
        # metrics identifier
        is_applied=True,
        metric_id=metric_id,
        # contained data
        time_resolution=time_resolution,
        time_start=data.get_time_start(),
        time_end=data.get_time_end(),
        data=data,
        # references to other services
        # TODO add useful values here
        language_id=0,
        creator_path=creator_path,
        unit_id=unit_id,
        indicator_id=indicator_id,
        class_id=class_id)

    return dataset_api.store(dataset)
