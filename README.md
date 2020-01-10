# emg-backlog-schema

Django project and app for the backlog schema.

This project is intended to be used as a cli or a lib, but it is hosted on the dev machine on for admin purposes.

## Installation

### Python version support
3.4, 3.5, 3.6

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
emgbacklog.py migrate --database {default|dev|prod}
```
