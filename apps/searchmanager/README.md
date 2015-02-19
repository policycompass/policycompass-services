# Search Manager
Provides indexing services for elastic search.Thereafter in the frontend you can use the searchclient service of the pcApp.search.services.search to make any kind of search query.

## Manual

### Elastic search setup
* Download the elasticsearch  from http://www.elasticsearch.org/download/
* Unzip elasticsearch into a folder
* Run ./bin/elasticsearch
* Check elasticsearch URL setting in policycompass-services/settings.py (should be ok by default localhost:9200)
* With elasticsearch and policy-compass backend services running execute the following command to rebuild index
```shell
	python manage.py rebuild_index
```
More indexing services are described in the next section

### Indexing using django command

* To index all documents of all item types (metrics,visualizations,events) type 
```shell
  python manage.py rebuild_index
```
* To index all documents but only specific item types (metrics,visualizations or events) type 
```shell
  python manage.py rebuild_index 'itemtype1' 'itemtype2' etc
```
* For instance to index all documents but of type metric and event only
```shell
  python manage.py rebuild_index 'metric' 'visualization'
```

### Indexing using web services
* All indexing services are described in
```shell
  http://localhost:8000/api/v1/searchmanager/
```

* To index all documents of all item types (metrics,visualizations,events) type 
```shell
  curl -XPOST 'http://localhost:8000/api/v1/searchmanager/rebuildindex'
```
* To index all documents but only specific item type (metrics,visualizations or events) type 
```shell
  curl -XPOST 'http://localhost:8000/api/v1/searchmanager/rebuildindex_<itemtype>'
```
* For instance to index metrics only
```shell
  curl -XPOST 'http://localhost:8000/api/v1/searchmanager/rebuildindex_metric'
```

### Create or update the index of a specific item using web services
* When you create / update an item you can call the following methods afterwards to update the search index
```shell
  curl -XPOST 'http://localhost:8000/api/v1/searchmanager/updateindexitem/<itemtype>/<itemid>
```
where <itemtype> is either 'metric','visualization' or 'event' and itemid the id of your created / updated object

* For instance to update the index of metric with id 26
```shell
  curl -XPOST 'http://localhost:8000/api/v1/searchmanager/updateindexitem/metric/26
```

### Delete the index of a specific item using web services
* When you delete an item in your database you can call the following methods afterwards to delete also the search index of that particular object
```shell
  curl -XPOST 'http://localhost:8000/api/v1/searchmanager/deleteindexitem/<itemtype>/<itemid>
```
where <itemtype> is either 'metric','visualization' or 'event' and itemid the id of your created / updated object

* For instance to delete the index of metric with id 26
```shell
  curl -XPOST 'http://localhost:8000/api/v1/searchmanager/deleteindexitem/metric/26

