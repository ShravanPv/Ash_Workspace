import random
import signal
import sys
import time
from datetime import datetime
from logging import getLogger
from logging.config import dictConfig

import config

dictConfig(config.LOGGING)
logger = getLogger('alerts')


def create_alert():
    body = [
        {
            'measurement': 'missed_files',
            'tags': {
                'instance_id': random.randint(1, 10),
            },
            'time': datetime.utcnow(),
            'fields': {
                'missed_files': random.randint(0, 100)
            }
        },
        {
            'measurement': 'stuck_in_ucm',
            'tags': {
                'instance_id': random.randint(1, 10),
            },
            'time': datetime.utcnow(),
            'fields': {
                'count': random.randint(0, 75)
            }
        },
        {
            'measurement': 'terminal_errors',
            'tags': {
                'instance_id': random.randint(1, 10),
            },
            'time': datetime.utcnow(),
            'fields': {
                'count': random.randint(0, 25)
            }
        },
        {
            'measurement': 'business_errors',
            'tags': {
                'instance_id': random.randint(1, 10),
            },
            'time': datetime.utcnow(),
            'fields': {
                'count': random.randint(0, 50)
            }
        }
    ]
    logger.info(f'the request body is: {body}')


def signal_handler(sig, frame):
    del sig, frame
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    logger.info('sending metrics to influxdb...')
    print('Press Ctrl+C to exit')
    while True:
        create_alert()
        time.sleep(60)
