from functools import wraps

from flask_restful import abort
from werkzeug.exceptions import UnprocessableEntity


class InternalServerError(Exception):
    pass


def handle_exceptions():
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except ValueError as val_err:
                abort(400, message=val_err.args)
            except UnprocessableEntity as unprocessable_entity:
                abort(422, **unprocessable_entity.data)
            except InternalServerError as internal_err:
                abort(500, message=internal_err.args)

        return wrapped

    return wrapper
