#!/usr/bin/env python

import os
import sys

import pkg_resources


def main():
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
  try:
    import django
  except ImportError as exc:
    raise ImportError(
      "Couldn't import Django. Are you sure it's installed and "
      "available on your PYTHONPATH environment variable? Did you "
      "forget to activate a virtual environment?"
    ) from exc

  django.setup()
  from django.core.management.commands.runserver import Command
  Command.default_port = django.conf.settings.RUNSERVER
  from django.core.management import execute_from_command_line
  execute_from_command_line(sys.argv)


if __name__ == '__main__':
  main()
