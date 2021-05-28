# -*- coding: utf-8 -*-

import pipeline
from pipeline.signals import (
  css_compressed,
  js_compressed,
)


del pipeline

INSTALLED_APPS.append('pipeline')

STATICFILES_STORAGE = (
  'pipeline.storage.PipelineStorage'
)

try:
  STATICFILES_FINDERS
except NameError:
  from django.conf.global_settings import (
    STATICFILES_FINDERS
  )
STATICFILES_FINDERS.append(
  'pipeline.finders.PipelineFinder'
)

PIPELINE = {
  #'PIPELINE_ENABLED': True,

  'JAVASCRIPT': {},
  'STYLESHEETS': {},

  'CSS_COMPRESSOR': 'pipeline.compressors.csshtmljsminify.CssHtmlJsMinifyCompressor',
  'JS_COMPRESSOR': 'pipeline.compressors.csshtmljsminify.CssHtmlJsMinifyCompressor',
}

# Poista JS- ja CSS-lähdekoodi paketoinnin jälkeen.
def poista_lahdekoodi(sender, *, package, **kwargs):
  for lahde in package.sources:
    sender.compressor.storage.delete(lahde)
css_compressed.connect(poista_lahdekoodi)
js_compressed.connect(poista_lahdekoodi)

del css_compressed
del js_compressed
