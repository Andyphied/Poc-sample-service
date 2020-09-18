from celery.schedules import crontab
from datetime import timedelta

CELERY_TIMEZONE = 'UTC'

CELERY_TASK_SERILAIZER = 'json'

CELERY_RESULT_SERILAIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'update mongodb database': {
        'task': 'New_Data in Mongo',
        'schedule': crontab()
        },
    'update sql database': {
        'task': 'Update Sql Data',
        'schedule': timedelta(minutes=1)
        },
    }
