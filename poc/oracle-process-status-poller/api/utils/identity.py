from functools import wraps


def get_current_identity():
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            current_identity = get_jwt_identity()
            instance_id = current_identity['instance_id']
            user_id = current_identity['user_id']
            username = current_identity['username']
            is_admin = current_identity.get('is_admin', False)
            is_superuser = current_identity.get('is_superuser', False)

            http_origin = get_user_origin()
            db_uri = get_client_db_uri(http_origin)
            # TODO : check whether instance_id matches http origin

            engine = create_engine(db_uri)
            session = sessionmaker(bind=engine)
            client_session = session()
            g.session = client_session
            g.current_user_identity = {
                'user_id': user_id,
                'username': username,
                'is_admin': is_admin,
                'is_superuser': is_superuser
            }

            if not is_superuser:
                get_client_user(username, client_session)

            return fn(instance_id, user_id, username, is_admin, is_superuser,
                      http_origin, *args, **kwargs)

        return wrapped

    return wrapper
