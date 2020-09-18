import os
from flask import Flask
from flask_restplus import Api
from operators_backend.task import init_celery

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


def create_app(app_name=PKG_NAME, **kwargs):
    from operators_backend.api_namespace import api_namespace
    from operators_backend.admin_namespace import admin_namespace

    application = Flask(__name__)
    api = Api(application, version='0.1', title='Operators Backend API',
              description='A Zeno CRUD API')

    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), application)

    from operators_backend.db import db, mongo, db_config, mongo_config
    application.config['RESTPLUS_MASK_SWAGGER'] = False
    application.config['MONGODB_SETTINGS'] = mongo_config
    application.config.update(db_config)
    db.init_app(application)
    mongo.init_app(application)
    application.db = db
    application.mongo = mongo

    api.add_namespace(api_namespace)
    api.add_namespace(admin_namespace)

    return application
