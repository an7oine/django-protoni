# -*- coding: utf-8 -*-

import django_heroku

django_heroku.settings(locals())

if not isinstance(MIDDLEWARE, list):
  MIDDLEWARE = list(MIDDLEWARE)
