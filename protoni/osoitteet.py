# -*- coding: utf-8 -*-

from django.conf import settings
from django import forms
from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic import View
import pkg_resources


class Index(View):
  def get(self, request):
    if 'django.contrib.auth' in settings.INSTALLED_APPS \
    and not request.user.is_authenticated:
      return redirect(settings.LOGIN_URL)
    else:
      return redirect(settings.LOGIN_REDIRECT_URL)
  # class Index


urlpatterns = [
  path('', Index.as_view(), name='index'),
]


# Lisää kiinteät näkymät.
for entry_point in pkg_resources.iter_entry_points('django.nakymat'):
  try:
    moduuli = entry_point.load()
  except ImportError:
    pass
  else:
    urlpatterns.append(
      path(
        entry_point.name + '/',
        include(moduuli)
      )
    )
    # else
  # for entry_point in pkg_resources.iter_entry_points


# Lisää asennetut osoitteistot.
for entry_point in pkg_resources.iter_entry_points('django.osoitteisto'):
  urlpatterns.append(
    path(
      entry_point.name + '/',
      include((entry_point.module_name, entry_point.name)),
    )
  )
  # for entry_point in pkg_resources.iter_entry_points
