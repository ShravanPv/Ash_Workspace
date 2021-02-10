from flask_restful import Api


def create_restful_api(app):
    api = Api(app)

    api.add_resource(HelloWorld, '/poc/poller')
