# -*- coding: utf-8 -*-

import os
import pkg_resources

from django.core.asgi import get_asgi_application


# pylint: disable=not-an-iterable
for paketti in pkg_resources.working_set:
  if not paketti.has_metadata('RECORD') and os.path.commonpath(
    (__file__, paketti.location)
  ) == paketti.location:
    # Mikäli `protoni` on asennettu kehitystilassa
    # (`python setup.py develop`), käytetään oletuksena testiasetuksia.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protoni.tyoasema')
    break
else:
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protoni.palvelin')


django = get_asgi_application()

try:
  from pistoke.kasittelija import WebsocketKasittelija
except ModuleNotFoundError:
  async def websocket(*args):
    raise NotImplementedError('Pistoke-pakettia ei ole asennettu!')
else:
  websocket = WebsocketKasittelija()


async def application(scope, receive, send):
  if scope['type'] == 'http':
    return await django(scope, receive, send)
  elif scope['type'] == 'websocket':
    return await websocket(scope, receive, send)
  else:
    raise NotImplementedError(f'Tuntematon pyyntö {scope["type"]}')
  # async def application
