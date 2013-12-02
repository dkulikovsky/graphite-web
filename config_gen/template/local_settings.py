TIME_ZONE = 'Europe/Moscow'

DOCUMENTATION_URL = "http://graphite.readthedocs.org/"

DEFAULT_CACHE_DURATION = 300

LOG_RENDERING_PERFORMANCE = True
LOG_CACHE_PERFORMANCE = True
LOG_METRIC_ACCESS = True

GRAPHITE_ROOT = '/opt/graphite'

CONF_DIR = '/opt/graphite/conf'
STORAGE_DIR = '/opt/graphite/storage'
CONTENT_DIR = '/opt/graphite/webapp/content'

DASHBOARD_CONF = '/opt/graphite/conf/dashboard.conf'
GRAPHTEMPLATES_CONF = '/opt/graphite/conf/graphTemplates.conf'

CERES_DIR = '/opt/graphite/storage/ceres'
LOG_DIR = '/opt/graphite/storage/log/webapp'
INDEX_FILE = '/opt/graphite/storage/index'  # Search index file
DATABASE_ENGINE = 'django.db.backends.mysql'
DATABASE_NAME = 'graphite'      # Or path to the database file if using sqlite3
DATABASE_USER = 'graphite'
DATABASE_PASSWORD = 'etihparg'
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = '3306'
