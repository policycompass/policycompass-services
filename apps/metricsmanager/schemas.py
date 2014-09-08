"""
Defines the JSON Hyper-Schemas with the help of Python data structures.
"""

from collections import OrderedDict
from rest_framework.reverse import reverse

class Schemas(object):
    """
    Defines the JSON Hyper-Schemas with the help of Python data structures.
    """
    def get_schema(self, ident, request):
        """
        Returns a specific schema.
        The responsible function is determined by adding _schema to the ident parameter.
        """
        result = getattr(self, '_' + ident + '_schema')(request)
        return result

    def _category_schema(self, request):
        """
        Schema for a category.
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('category',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for a category'
        s['type'] = 'object'
        s['links'] = [
            OrderedDict([
                ('title', 'Get a collection of categories'),
                ('rel', 'collection'),
                ('href', reverse('extra-list')),
                ('method', 'GET'),
                ('mediaType', 'application/json')
            ])]
        s['properties'] = self._category_properties(request)

        return s


    def _category_collection_schema(self, request):
        """
        Schema for a list of categories
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('category_collection',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for a category collection'
        s['type'] = 'array'
        s['links'] = [
            OrderedDict([
                ('title', 'Get one category'),
                ('rel', 'item'),
                ('href', reverse('extra-list') + '/{id}'),
                ('method', 'GET'),
                ('mediaType', 'application/json')
            ])]
        s['items'] = OrderedDict([
                    ('description', 'One category'),
                    ('type', 'object'),
                    ('properties', self._category_properties(request))
        ])
        return s

    def _category_properties(self, request):
        """
        Properties of a category.
        """
        p = OrderedDict([
            ('id', OrderedDict([
                ('description', 'Unique Identifier of the category'),
                ('type', 'number'),
            ])),
            ('title', OrderedDict([
                ('title', 'The title of the category'),
                ('type', 'string'),
            ])),
            ('description', OrderedDict([
                ('title', 'The description of the category'),
                ('type', 'string'),
            ]))
        ])
        return p


    def _converter_schema(self, request):
        """
        Schema for the converter.
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('converter',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for the converter'
        s['type'] = 'object'
        s['links'] = [
             OrderedDict([
                ('title', 'Convert a file'),
                ('rel', 'convert'),
                ('href', reverse('converter')),
                ('method', 'POST'),
                ('mediaType', 'application/json'),
                ('encType', 'multipart/form-data'),
            ])
        ]
        return s

    def _converter_result_schema(self, request):
        """
        Schema for the result of a conversion.
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('converter_result',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for a converter result'
        s['type'] = 'object'
        s['properties'] = [
            OrderedDict([
                ('filesize', OrderedDict([
                    ('description', 'The size of the posted file in kB'),
                    ('type', 'integer')
                ])),
                ('filename', OrderedDict([
                    ('description', 'The name of the posted file'),
                    ('type', 'string')
                ])),
                ('result', OrderedDict([
                    ('description', 'The result of the conversion'),
                    ('type', 'array'),
                    ('items', OrderedDict([
                        ('description', 'The rows of the result'),
                        ('type', 'array'),
                        ('items', OrderedDict([
                            ('description', 'The columns of the result'),
                            ('type', 'string'),
                        ]))
                    ]))
                ]))

            ])
        ]
        s['links'] = [
             OrderedDict([
                ('title', 'Convert a file'),
                ('rel', 'convert'),
                ('href', reverse('converter')),
                ('method', 'POST'),
                ('mediaType', 'application/json'),
                ('encType', 'multipart/form-data'),
            ])
        ]
        return s

    def _metrics_manager_schema(self, request):
        """
        Schema for the base resource of the Metrics Manager
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('metrics_manager',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for the metrics manager'
        s['type'] = 'object'
        s['links'] = [
             OrderedDict([
                ('title', 'Get the metric resource'),
                ('rel', 'collection'),
                ('href', reverse('metric-list')),
                ('method', 'GET'),
                ('mediaType', 'application/json')
            ]),
            OrderedDict([
                ('title', 'Get the extra categories resource'),
                ('rel', 'collection'),
                ('href', reverse('extra-list')),
                ('method', 'GET'),
                ('mediaType', 'application/json')
            ]),
            OrderedDict([
                ('title', 'Get the converter resource'),
                ('rel', 'item'),
                ('href', reverse('converter')),
                ('method', 'GET'),
                ('mediaType', 'application/json')
            ]),
        ]
        s['properties'] = OrderedDict([
            ('Metrics', OrderedDict([
                ('description', 'Link to the metrics resource'),
                ('type', 'string')
            ])),
            ('Extra Categories', OrderedDict([
                ('description', 'Link to the extra categories resource'),
                ('type', 'string')
            ])),
            ('Converter', OrderedDict([
                ('description', 'Link to the converter resource'),
                ('type', 'string')
            ]))
        ])

        return s

    def _metric_collection_schema(self, request):
        """
        Schema for the list of metrics,
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('metric_collection',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for a metric collection'
        s['type'] = 'object'
        s['links'] = self._metric_collection_links(request)
        s['properties'] = self._metric_collection_properties(request)

        return s

    def _metric_collection_properties(self, request):
        """
        Properties of the list of metrics.
        """
        p = OrderedDict()

        p['count'] = OrderedDict([
            ('description', 'Total number of metrics in the collection'),
            ('type', 'integer')
        ])
        p['next'] = OrderedDict([
            ('description', 'Link to the next page of the collection'),
            ('type', 'string')
        ])
        p['previous'] = OrderedDict([
            ('description', 'Link to the previous page of the collection'),
            ('type', 'string')
        ])

        metric_properties = self._metric_properties(request)
        metric_properties.pop('data')
        p['results'] = OrderedDict([
            ('description', 'The collection of metrics'),
            ('type', 'array'),
            ('items', OrderedDict([
                ('description', 'A metric object'),
                ('type', 'object'),
                ('properties', metric_properties)
            ]))
        ])
        return p

    def _metric_collection_links(self, request):
        """
        Links of the list of metrics.
        """
        l = [
            OrderedDict([
                ('title', 'Get one metric, including metric data'),
                ('rel', 'item'),
                ('href', reverse('metric-list') + '/{id}'),
                ('method', 'GET'),
                ('mediaType', 'application/json')
            ]),
            OrderedDict([
                ('title', 'Filter the metric collection'),
                ('rel', 'filter'),
                ('href', reverse('metric-list')),
                ('method', 'GET'),
                ('mediaType', 'application/json'),
                ('encType', 'application/x-www-form-urlencode'),
                ('schema', OrderedDict([
                    ('type', 'object'),
                    ('properties', OrderedDict([
                        ('page', OrderedDict([
                            ('description', 'Select the page of the list'),
                            ('type', 'integer')
                        ])),
                        ('search', OrderedDict([
                            ('description', 'Search in title, keywords, acronym and spatial'),
                            ('type', 'string')
                        ])),
                        ('sort', OrderedDict([
                            ('description', 'Sort the collection: Values: created_at, updated_at or title. A leading - reverses the order'),
                            ('type', 'string')
                        ])),
                        ('language', OrderedDict([
                            ('description', 'Filter the collection by a language ID'),
                            ('type', 'integer')
                        ])),
                        ('unit', OrderedDict([
                            ('description', 'Filter the collection by a unit ID'),
                            ('type', 'integer')
                        ])),
                        ('external_resource', OrderedDict([
                            ('description', 'Filter the collection by a external resource ID'),
                            ('type', 'integer')
                        ])),
                        ('policy_domain', OrderedDict([
                            ('description', 'Filter the collection by a policy domain ID'),
                            ('type', 'integer')
                        ]))
                    ]))
                ]))
            ]),
            OrderedDict([
                ('title', 'Create a new metric'),
                ('rel', 'create'),
                ('href', reverse('metric-list')),
                ('method', 'POST'),
                ('mediaType', 'application/json'),
                ('encType', 'application/json'),
                ('schema', OrderedDict([
                    ('type', 'object'),
                    ('$ref', reverse('schema-detail', request=request, args=('metric_create',))),
                    ('required', [
                        'title',
                        'acronym',
                        'description',
                        'keywords',
                        'unit',
                        'language',
                        'policy_domains',
                        'data',
                        'user_id'
                    ])
                ]))
            ]),
        ]
        return l



    def _metric_schema(self, request):
        """
        Schema for a metric.
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('metric',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for a metric'
        s['type'] = 'object'
        s['links'] = self._metric_links(request)
        s['properties'] = self._metric_properties(request)

        return s

    def _metric_create_schema(self, request):
        """
        Schema for creating a metric
        """
        # Based on properties for a metric in read mode
        s = self._metric_properties(request)
        # Pop read-only fields
        s.pop('self')
        s.pop('issued')
        s.pop('modified')
        s.pop('id')
        s.pop('version')
        s.pop('unit')
        s['unit'] = OrderedDict([
            ('description', 'An ID of an unit'),
            ('type', 'integer')
        ])

        s['data']['properties'].pop('ranges')
        s['data']['properties']['table']['items']['properties'].pop('row')
        s.pop('language')
        s['language'] = OrderedDict([
            ('description', 'An ID of an language'),
            ('type', 'integer')
        ])
        s.pop('external_resource')
        s['external_resource'] = OrderedDict([
            ('description', 'An ID of an external resource'),
            ('type', 'integer')
        ])

        return s

    def _metric_links(self, request):
        """
        Links of a metric resource.
        """
        l = [
            OrderedDict([
                ('title', 'List of all metrics'),
                ('rel', 'collection'),
                ('href', reverse('metric-list')),
                ('method', 'GET'),
                ('mediaType', 'application/json')
            ]),
            OrderedDict([
                ('title', 'Filter the metric data'),
                ('rel', 'filter'),
                ('href', reverse('metric-list') + '/{id}'),
                ('method', 'GET'),
                ('mediaType', 'application/json'),
                ('encType', 'application/x-www-form-urlencode'),
                ('schema', OrderedDict([
                    ('type', 'object'),
                    ('properties', OrderedDict([
                        ('sort', OrderedDict([
                            ('description', 'Sorting order of the metric data'),
                            ('type', 'string')
                        ])),
                    ('additionalProperties', True)
                    ]))
                ]))
            ]),
            OrderedDict([
                ('title', 'Edit this metric'),
                ('rel', 'update'),
                ('href', reverse('metric-list') + '/{id}'),
                ('method', 'PUT'),
                ('mediaType', 'application/json'),
                ('encType', 'application/json'),
                ('schema', OrderedDict([
                    ('type', 'object'),
                    ('$ref', reverse('schema-detail', request=request, args=('metric_create',))),
                    ('required', [
                        'title',
                        'acronym',
                        'description',
                        'keywords',
                        'unit',
                        'language',
                        'policy_domains'
                    ])
                ]))
            ]),
            OrderedDict([
                ('title', 'Delete this metric'),
                ('rel', 'delete'),
                ('href', reverse('metric-list') + '/{id}'),
                ('method', 'DELETE'),
                ('mediaType', 'application/json')
            ])
        ]
        return l


    def _metric_properties(self, request):
        """
        Properties of a metric.
        """
        p = OrderedDict()

        p['self'] = OrderedDict([
            ('description', 'URI of the metric'),
            ('type', 'string')
        ])
        p['spatial'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/spatial'),
            ('type', 'string')
        ])
        p['resource_url'] = OrderedDict([
            ('description', 'https://schema.org/isBasedOnUrl'),
            ('type', 'string')
        ])
        p['unit'] = OrderedDict([
            ('type', 'object'),
            ('$ref', reverse('schema-detail', request=request, args=('unit',)))
        ])
        p['language'] = OrderedDict([
            ('type', 'object'),
            ('$ref', reverse('schema-detail', request=request, args=('language',)))
        ])
        p['external_resource'] = OrderedDict([
            ('type', 'object'),
            ('$ref', reverse('schema-detail', request=request, args=('external_resource',)))
        ])
        p['resource_issued'] = OrderedDict([
            ('description', 'The date the resource was issued, refering to resource_url'),
            ('type', 'string')
        ])
        p['issued'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/issued'),
            ('type', 'string')
        ])
        p['modified'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/modified'),
            ('type', 'string')
        ])
        p['policy_domains'] = OrderedDict([
            ('description', 'The policy domains associated with this metric'),
            ('type', 'array'),
            ('items', OrderedDict([
                ('description', 'Policy domain object'),
                ('type', 'object'),
                ('properties', self._policy_domain_schema(request))
            ]))
        ])
        p['data'] = OrderedDict([
            ('description', 'The actual data of the metric'),
            ('type', 'object'),
            ('properties', self._metric_data_schema(request))
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the metric'),
            ('type', 'integer')
        ])
        p['title'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/title'),
            ('type', 'string')
        ])
        p['acronym'] = OrderedDict([
            ('description', 'A shorter title for the metric'),
            ('type', 'string')
        ])
        p['description'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/description'),
            ('type', 'string')
        ])
        p['keywords'] = OrderedDict([
            ('description', 'http://schema.org/keywords'),
            ('type', 'string')
        ])
        p['publisher'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/publisher'),
            ('type', 'string')
        ])
        p['license'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/license'),
            ('type', 'string')
        ])
        p['version'] = OrderedDict([
            ('description', 'https://schema.org/version'),
            ('type', 'integer')
        ])
        p['user_id'] = OrderedDict([
            ('description', 'The ID of the Policy Compass User'),
            ('type', 'integer')
        ])
        p['formula'] = OrderedDict([
            ('description', 'The calculation formula for a derived metric'),
            ('type', 'string')
        ])

        return p

    def _metric_data_schema(self, request):
        """
        Schema for the raw data of a metric
        """
        p = OrderedDict()

        p['ranges'] = OrderedDict([
            ('description', 'The actual ranges of extra columns'),
            ('type', 'object')
        ])

        p['extra_columns'] = OrderedDict([
            ('description', 'Extra columns used in the table'),
            ('type', 'array'),
            ('items', OrderedDict([
                ('description', 'Column-Names'),
                ('type', 'string'),
            ]))
        ])
        p['table'] = OrderedDict([
            ('description', 'Tabular data of the metric'),
            ('type', 'array'),
            ('items', OrderedDict([
                ('description', 'List of table rows'),
                ('type', 'object'),
                ('properties', OrderedDict([
                    ('row', OrderedDict([
                        ('description', 'The number of the row'),
                        ('type', 'integer')
                    ])),
                    ('from', OrderedDict([
                        ('description', 'The from-date of the row'),
                        ('type', 'string')
                    ])),
                    ('to', OrderedDict([
                        ('description', 'The to-date of the row'),
                        ('type', 'string')
                    ])),
                    ('value', OrderedDict([
                        ('description', 'The value of the row'),
                        ('type', 'number')
                    ]))
                ])),

                ('additionalProperties', True)
            ]))
        ])


        return p

    def _policy_domain_schema(self, request):
        """
        Sub-Schema for the policy domains in a metric.
        """
        p = OrderedDict()

        p['title'] = OrderedDict([
            ('description', 'Title of the policy domain'),
            ('type', 'string')
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the policy domain'),
            ('type', 'integer')
        ])
        p['description'] = OrderedDict([
            ('description', 'Description of the policy domain'),
            ('type', 'string'),
        ])

        return p


    def _external_resource_schema(self, request):
        """
        Sub-Schema for the external resource.
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('external_resource',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for an external resource'
        s['type'] = 'object'
        s['properties'] = self._external_resource_properties(request)

        return s

    def _external_resource_properties(self, request):
        """
        Properties of a external resource.
        """
        p = OrderedDict()

        p['title'] = OrderedDict([
            ('description', 'Title of the external resource'),
            ('type', 'string')
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the external resource'),
            ('type', 'integer')
        ])
        p['url'] = OrderedDict([
            ('description', 'URL of the external resource'),
            ('type', 'string'),
        ])
        p['api_url'] = OrderedDict([
            ('description', 'URL of the API of the external resource'),
            ('type', 'string'),
        ])

        return p


    def _language_schema(self, request):
        """
        Sub-Schema for a language.
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('unit',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for an language'
        s['type'] = 'object'
        s['properties'] = self._language_properties(request)

        return s

    def _language_properties(self, request):
        """
        Properties of a language
        """
        p = OrderedDict()

        p['title'] = OrderedDict([
            ('description', 'Title of the language'),
            ('type', 'string')
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the language'),
            ('type', 'integer')
        ])
        p['code'] = OrderedDict([
            ('description', 'Unique code of the language'),
            ('type', 'string'),
            ('maxLength', 2),
            ('minLength', 2),
        ])
        return p

    def _unit_schema(self, request):
        """
        Sub-Schema for the unit.
        """
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('unit',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for an unit'
        s['type'] = 'object'
        s['properties'] = self._unit_properties(request)

        return s

    def _unit_properties(self, request):
        """
        Properties of a unit.
        """
        p = OrderedDict()

        p['description'] = OrderedDict([
            ('description', 'Description of the unit'),
            ('type', 'string')
        ])
        p['title'] = OrderedDict([
            ('description', 'Title of the unit'),
            ('type', 'string')
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the unit'),
            ('type', 'integer')
        ])
        p['unit_category'] = OrderedDict([
            ('description', 'The category of the unit'),
            ('type', 'object'),
            ('properties', OrderedDict([
                ('id', OrderedDict([
                    ('description', 'Unique identifier of the unit category'),
                    ('type', 'integer')
                ])),
                ('title', OrderedDict([
                    ('description', 'Title of the unit category'),
                    ('type', 'string')
                ]))
            ]))
        ])


        return p
