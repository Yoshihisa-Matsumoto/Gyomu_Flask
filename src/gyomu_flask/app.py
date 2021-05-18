import os
from flask import Flask, request
from flask_restful import Api
from gyomu_flask.resources.gyomu_apps import GyomuAppListResource, GyomuAppResource

def create_app():
    env = os.environ.get('ENV', 'Development')
    if env == 'Production':
        config_str = 'gyomu_flask.config.ProductionConfig'
    elif env == 'Staging':
        config_str = 'gyomu_flask.config.StagingConfig'
    else:
        config_str = 'gyomu_flask.config.DevelopmentConfig'

    app = Flask(__name__)
    app.config.from_object(config_str)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    pass


def register_resources(app):
    api = Api(app)
    api.add_resource(GyomuAppListResource,'/apps')
    api.add_resource(GyomuAppResource,'/apps/<int:application_id>')

if __name__ == '__main__':
    #print(os.environ.get('GYOMU_COMMON_MAINDB_CONNECTION','none?'))
    app = create_app()
    app.run()
