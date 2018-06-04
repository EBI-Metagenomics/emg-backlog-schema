# emg-backlog-schema
DjangoDB project and app for the backlog schema.
## Installation
### Python version support
3.4, 3.5, 3.6
### Pip package
```bash
pip install -U git+git://github.com/EBI-Metagenomics/emg-backlog-schema.git
```

### DB config files
An environment variable needs to be defined for each database config (DJANGO_BACKLOG_DEFAULT_CONFIG, DJANGO_BACKLOG_DEV_CONFIG, DJANGO_BACKLOG_PROD_CONFIG).
These should contain paths to yaml config files, which must contain the following fields at root level:
```yaml
ENGINE: 'django.db.backends.mysql'
HOST: 'host'
PORT: 3306 (or other)
DB: 'database_name'
NAME: 'schema_name'
USER: 'user'
PASSWORD: 'password'
```

### Create local database instance
```bash
emgbacklog migrate --database {default|dev|prod}
```
