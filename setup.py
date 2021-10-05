# -* - coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
  setup_requires='git-versiointi',
  name='django-protoni',
  packages=find_packages(),
  py_modules=['manage'],
  include_package_data=True,
  scripts=['manage.py'],
  install_requires=['Django', 'python-decouple'],
  entry_points={
    'django.nakymat': [
      '__debug__ = protoni.nakymat:DebugToolbar',
      'kirjaudu = protoni.nakymat:Kirjautuminen',
      'kanta = protoni.nakymat:Kanta',
    ],
    'django.asetukset': [
      'celery = protoni.laajennos.celery',
      'debug_toolbar = protoni.laajennos.debug_toolbar',
      'dj_database_url = protoni.laajennos.dj_database_url',
      'heroku = protoni.laajennos.heroku',
      'pipeline = protoni.laajennos.pipeline',
    ],
  },
)
