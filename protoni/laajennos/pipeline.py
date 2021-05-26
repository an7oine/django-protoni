# -*- coding: utf-8 -*-

import pipeline
del pipeline

INSTALLED_APPS.append('pipeline')

STATICFILES_STORAGE = (
  'pipeline.storage.PipelineManifestStorage'
)

#try:
#  STATICFILES_FINDERS
#except NameError:
#  from django.conf.global_settings import (
#    STATICFILES_FINDERS
#  )
#STATICFILES_FINDERS.append(
#  'pipeline.finders.PipelineFinder'
#)
STATICFILES_FINDERS = (
  'pipeline.finders.FileSystemFinder',
  'pipeline.finders.AppDirectoriesFinder',
  'pipeline.finders.CachedFileFinder',
  'pipeline.finders.PipelineFinder',
)

PIPELINE = {
  #'PIPELINE_ENABLED': True,

  'JAVASCRIPT': {},
  'STYLESHEETS': {},

  'CSS_COMPRESSOR': 'pipeline.compressors.csshtmljsminify.CssHtmlJsMinifyCompressor',
  'JS_COMPRESSOR': 'pipeline.compressors.csshtmljsminify.CssHtmlJsMinifyCompressor',
}
