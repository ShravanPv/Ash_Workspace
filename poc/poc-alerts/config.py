import os
from os import path

INFLUX_HOST = os.environ.get('INFLUX_HOST')
INFLUX_PORT = os.environ.get('INFLUX_PORT')
INFLUX_USER = os.environ.get('INFLUX_USER')
INFLUX_PASSWORD = os.environ.get('INFLUX_PASSWORD')
INFLUX_DATABASE = os.environ.get('INFLUX_DATABASE')

pwd = path.dirname(path.realpath('__file__'))
log_dir = 'logs'
log_file = 'alerts.log'
log_dir_path = os.path.join(pwd, log_dir)

if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'compact': {
            'format': '%(asctime)s [%(levelname)-8.8s] %(name)-10.10s : '
                      '%(message)s'
        },
        'verbose': {
            'format': '%(process)d %(asctime)s [%(levelname)s] %(name)s '
                      '[%(filename)-s:%(lineno)-s] [%(funcName)s]: %(message)s'
        },
        'err_report': {
            'format': '%(asctime)s\n%(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'alerts': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
            'filename': os.path.join(log_dir_path, log_file),
            'interval': 1,
            'when': 'midnight',
            'encoding': 'utf8'
        }
    },
    'loggers': {
        'alerts': {
            'handlers': ['alerts', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
