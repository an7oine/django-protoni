# -*- coding: utf-8 -*-

'''
Sentry-SDK-käyttöönotto. Edellyttää seuraavien muuttujien määrityksen:
- SENTRY_DSN: Sentry-palvelimen yhteysosoite
- SENTRY_PAKETTIVERSIO: sen Pip-paketin nimi, jonka versionumero
  ilmoitetaan Sentrylle.
'''
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Poimi DSN-yhteysosoite.
try:
  dsn = CONFIG('SENTRY_DSN')
except UndefinedValueError:
  raise ImportError

# Poimi sen paketin nimi, jonka versionumero ilmoitetaan Sentrylle.
try:
  paketti = CONFIG('SENTRY_PAKETTIVERSIO')
except UndefinedValueError:
  del dsn
  raise ImportError

# Poimi paketin versionumero.
from importlib.metadata import PackageNotFoundError, version
try:
  versio = version(paketti)
except PackageNotFoundError:
  del dsn
  raise ImportError
finally:
  del paketti
  del PackageNotFoundError, version

# Alusta Sentry-määritys.
# Ks. https://docs.sentry.io/platforms/python/guides/django/
sentry_sdk.init(
  dsn=dsn,
  release=versio,
  integrations=[DjangoIntegration()],
  send_default_pii=True,
)
del sentry_sdk, DjangoIntegration
del dsn, versio
