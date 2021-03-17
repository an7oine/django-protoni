# -*- coding: utf-8 -*-

import celery
del celery

CELERY_BROKER_URL = CONFIG('CELERY_BROKER_URL', default='redis://localhost:6379')
