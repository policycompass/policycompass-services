from collections import OrderedDict
from rest_framework.reverse import reverse
from django.templatetags.static import static


def metric_context(request):
    return _build_context(_metric_context(request))


def _metric_context(request):
    c = OrderedDict()

    c['spatial'] = 'http://purl.org/dc/terms/spatial'
    c['resource_url'] = 'https://schema.org/isBasedOnUrl'
    c['unit'] = reverse('unit-list', request=request)
    c['language'] = reverse('language-list', request=request)
    c['external_resource'] = reverse('resource-list', request=request)
    c['resource_issued'] = _local_schema(request, 'resource_issued')
    c['issued'] = 'http://purl.org/dc/terms/issued'
    c['modified'] = 'http://purl.org/dc/terms/modified'
    c['policy_domains'] = reverse('domain-list', request=request)
    c['data'] = _local_schema(request, 'metric_data')
    c['id'] = _local_schema(request, 'id')
    c['title'] = 'http://purl.org/dc/terms/title'
    c['acronym'] = _local_schema(request, 'acronym')
    c['description'] = 'http://purl.org/dc/terms/description'
    c['keywords'] = 'http://schema.org/keywords'
    c['publisher'] = 'http://purl.org/dc/terms/publisher'
    c['license'] = 'http://purl.org/dc/terms/license'
    c['version'] = 'https://schema.org/version'
    c['formula'] = _local_schema(request, 'formula')

    return c


def _build_context(context):
    c = OrderedDict()
    c['@context'] = context
    return c


def _expanded_term(id, type):
    c = OrderedDict
    c['@id'] = id
    c['@type'] = type
    return c


def _local_schema(request, id):
    return 'http://' + request.get_host() + '/static/schema.html#' + id
