from operators_backend import celery
from operators_backend.app import create_app
from operators_backend.task import init_celery

app = create_app()

init_celery(celery, app)
