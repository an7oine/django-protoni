# -*- coding: utf-8 -*-

import dj_database_url

# Tietokanta-asetukset muodostuvat `protoni.asetukset`-moduulissa vain,
# mikäli `DB_ENGINE` on määritetty. Luodaan tarvittaessa tyhjä pohja,
# jotta pelkkä `DATABASE_URL` riittää määritykseksi (Heroku, Railway).
try:
  DATABASES
except NameError:
  DATABASES = {'default': {}}

DATABASES['default'] = dj_database_url.config(
  conn_max_age=600,
  ssl_require=CONFIG('DB_SSL_REQUIRE', cast=bool, default=True),
) or DATABASES['default']
