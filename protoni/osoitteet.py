# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse
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

if 'django.contrib.auth' in settings.INSTALLED_APPS:
  from django.contrib.auth.views import LoginView, LogoutView
  urlpatterns += [
    path('kirjaudu-sisaan/', LoginView.as_view(
      template_name='kirjaudu-sisaan.html'
    ), name='kirjaudu-sisaan'),
    path('kirjaudu-ulos/', LogoutView.as_view(), name='kirjaudu-ulos'),
  ]

if 'django.contrib.admin' in settings.INSTALLED_APPS:
  from django.contrib import admin
  urlpatterns.append(path('kanta/', admin.site.urls))

# Lisää asennetut osoitteistot.
for entry_point in pkg_resources.iter_entry_points('django.osoitteet'):
  urlpatterns.append(
    path(
      entry_point.name + '/',
      include((entry_point.module_name, entry_point.name)),
    )
  )
