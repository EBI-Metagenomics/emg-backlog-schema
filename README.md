[![Build Status](https://travis-ci.org/EBI-Metagenomics/emg-backlog-schema.svg?branch=master)](https://travis-ci.org/EBI-Metagenomics/emg-backlog-schema)

# emg-backlog-schema
DjangoDB project and app for the backlog schema.
## Installation
### Python version support
3.5, 3.6, 3.7, 3.8

### Pip package
```bash
pip install -U git+git://github.com/EBI-Metagenomics/emg-backlog-schema.git
```

### DB config files
An environment variable named *BACKLOG_CONFIG* needs to be defined for the database config.
These should contain paths to yaml config file, which must contain the following fields:
```yaml
backlog:
  databases:
    default:
      ENGINE: 'django.db.backends.mysql'
      HOST: 'host'
      PORT: 3306 (or other)
      DB: 'database_name'
      NAME: 'schema_name'
      USER: 'user'
      PASSWORD: 'password'
    dev:
        ....
    prod:
        ....
```

### Create local database instance
```bash
emgbacklog migrate --database {default|dev|prod}
```

## Development
### How to set up your development environment (using Conda)?

```
    Install miniconda v3
    https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
    Add Conda binary path to your PATH
    $ export PATH="~/miniconda3/bin:$PATH"
    
    Clone GitHub repo onto your local machine:
    $ git clone git@github.com:EBI-Metagenomics/emg-backlog-schema.git
    $ cd emg-backlog-schema
    
    $ conda create -q -y -n backlog_cli python=3.6.9
    $ source activate backlog_cli 
    $ pip install -U -e .
    
    export BACKLOG_CONFIG=~/backlog-config.yaml
```

### How to create a new data migration?

    $ python backlog_cli/manage.py makemigrations --empty backlog --database {default|dev|prod}
    
### How to apply a (data) migration?

    $ python backlog_cli/manage.py migrate --database {default|dev|prod}