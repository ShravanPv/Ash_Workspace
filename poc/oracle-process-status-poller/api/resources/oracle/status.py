from celery import Celery
from flask import current_app as app, g, request
from flask_restful import Resource
from marshmallow import Schema, fields, validate
from webargs.flaskparser import use_kwargs

import config
from api.utils.exceptions import handle_exceptions

celery = Celery()
celery.config_from_object('config')


class OracleProcessStatusPostRequestFormat(Schema):
    params = fields.Dict(required=True)
    oracle_process_id = fields.Int(required=True)
    oracle_endpoint = fields.Str(required=True,
                                 validate=validate.Length(min=1))

    class Meta:
        strict = True


class ReconciliationListener(Resource):
    decorators = [get_reconciliation_db_session(), handle_exceptions()]

    def __init__(self):
        app.logger.info(f'In the constructor of {self.__class__.__name__}')

    @use_kwargs()
    def post(self):
        callback_payload = request.data
        oracle_request_id, summary_status, result = \
            parse_reconciliation_payload(callback_payload)

        erred = False
        if summary_status == 'ERROR':
            erred = True

        app.logger.info('getting reconciliation info')
        client_db_uri, file_id, reconciliation_id, oracle_endpoint, \
        oracle_username, oracle_password, \
        reconciliation_report_path = get_reconciliation_info(
            oracle_request_id, result, erred
        )
        g.session.commit()

        app.logger.info('sending reconciliation info to worker')
        celery.send_task(
            'worker.reconcile',
            (client_db_uri, file_id, reconciliation_id, oracle_endpoint,
             oracle_username, oracle_password, reconciliation_report_path),
            queue=config.RECONCILIATION_QUEUE_NAME
        )
        app.logger.info('successfully queued reconciliation task for '
                        f'reconciliation ID: {reconciliation_id}')
