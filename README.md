# Policy Compass Datamanager

## Installation

```shell
    apt-get install libpq-dev python-dev
```

* Create Python Virtualenv
* Clone Repository

```shell
	pip install -r requirements.txt
	python manage.py syncdb
	python manage.py migrate metrics_manager
	python manage.py loaddata metrics
	python manage.py runserver
```
