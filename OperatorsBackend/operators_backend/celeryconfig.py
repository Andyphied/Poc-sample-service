from celery.schedules import crontab

CELERY_TIMEZONE = 'UTC'

CELERY_TASK_SERILAIZER = 'json'

CELERY_RESULT_SERILAIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'update mongodb database': {
        'task': 'Update Mongo',
        'schedule': crontab()
        },
    'update sql database': {
        'task': 'Update Sql Data',
        'schedule': crontab(minute=0, hour=0)
        },
    }
