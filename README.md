# Policy Compass Services
Web Services for the Policy Compass


## Manual

This manual is tested under Ubuntu 14.04!

### Requirements

* Python 3.4 should be already installed, but make sure with the following command:
```shell
  python3
```
* Install the following packages:
```shell
  apt-get install python-virtualenv python3-dev libpq-dev
```
* Install SQLite (easier for development) or PostgreSQL:

Either do
```shell
  apt-get install sqlite3
```

or
```shell
  apt-get install postgresql
  pip install psycopg2==2.5.4
```

If you chose PostgreSQL, you want to create a postgres user and a database:

```shell
  sudo -u postgres createuser pcompass -W
  sudo -u postgres createdb pcompass --owner pcompass
```

### Installation
* Create a new directory for the project
```shell
  mkdir services
```
* Create a Python Virtual Environment with Python 3 and activate it
```shell
  virtualenv services --python=python3
  cd services
  source bin/activate
```
* Clone the repository including submodules
* Note: The submodule are configured for use with SSH, so configure your access to GitHub: https://help.github.com/articles/generating-ssh-keys
```shell
  git clone git@github.com:policycompass/policycompass-services.git
  cd policycompass-services
```
* Install the Requirements
```shell
  pip install -r requirements.txt
```
* Create a local settings file
```shell
  cp config/settings.sample.py config/settings.py
```
* Edit the settings.py according to your needs. See: https://docs.djangoproject.com/en/1.6/ref/settings/#databases
* Initialize the Database
```shell
	python manage.py migrate
    python manage.py syncdb
	python manage.py loaddata metrics events common references visualizations indicators ags
```

* Start the application
```shell
	python manage.py runserver
```
* Browse for example to: http://localhost:8000/api/v1/metrics

### Elastic search setup
* Download the elasticsearch  from http://www.elasticsearch.org/download/
* Unzip elasticsearch into a folder
* Run ./bin/elasticsearch
* Check elasticsearch URL setting in policycompass-services/settings.py (should be ok by default localhost:9200)
* With elasticsearch and policy-compass backend services running execute the following command to rebuild index
```shell
	python manage.py rebuild_index
```

## Coding style

All python code in this repository shall be compliant with the rules of pep8
and pyflakes except E501 (forbid long lines) and F403 (forbid `from xx import
*`) and they don't have to be applied to the django migration files.

Read the [flake8 docs](https://flake8.readthedocs.org) for a list of all rules.

The rules can be checked with the following command:

    bin/flake8 apps policycompass_services --ignore E501,F403 --exclude migrations

If the `Makefile` from the main policycompass repository is used, a pre commit
hook is installed, which checks for flake8 compliance as defined above. If this
repository is checked out manually and not as a submodule of the main
repository, you can create a pre commit hook manually by creating a file
`.git/hooks/pre-commit` with the following content:

    #!/bin/sh
    bin/flake8 apps policycompass_services --ignore E501,F403 --exclude migrations


## Policy Compass is Free Software

This project (i.e. all files in this repository if not declared otherwise) is
licensed under the GNU Affero General Public License (AGPLv3), see
LICENSE.txt.
