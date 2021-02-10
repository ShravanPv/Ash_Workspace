import os
from os import path


def boolean(x): return bool(int(x))


FLASK_APP_NAME = 'fusion-backend'
HOST = os.getenv('HOST', '127.0.0.1')
PORT = os.getenv('PORT', 5000)
DEBUG = boolean(os.environ.get('DEBUG', False))
TESTING = boolean(os.environ.get('TESTING', False))
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SCHEDULER_ENDPOINT = os.environ.get('SCHEDULER_ENDPOINT')

broker_url = os.environ.get('BROKER_URI')
worker_hijack_root_logger = bool(
    int(os.environ.get('WORKER_HIJACK_ROOT_LOGGER'))
)

pwd = path.dirname(path.realpath('__file__'))
logdir = 'logs'
logfile = 'api.log'

logdir_path = os.path.join(pwd, logdir)

if not os.path.exists(logdir_path):
    os.makedirs(logdir_path)

LOGGING_CONFIG = dict(
    version=1,
    formatters={
        'compact': {
            'format': '%(asctime)s [%(levelname)-8.8s] %(name)-10.10s : '
                      '%(message)s'
        },
        'verbose': {
            'format': '%(asctime)s [%(levelname)-8.8s] %(name)-8.8s '
                      '[%(filename)-15.15s:%(lineno)-3.3s]: %(message)s'
        },
        'err_report': {
            'format': '%(asctime)s\n%(message)s'
        }
    },
    handlers={
        'api': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
            'filename': os.path.join(logdir_path, logfile),
            'interval': 1,
            'when': 'midnight',
            'encoding': 'utf8'
        },
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    loggers={
        '': {
            'handlers': ['default'],
            'level': 'DEBUG'
        },
        'api': {
            'handlers': ['api'],
            'level': 'DEBUG',
            'propagate': False
        },
        'sqlalchemy.engine': {
            'level': 'INFO',
            'handlers': ['api']
        }
    }
)
