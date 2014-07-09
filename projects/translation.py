"""
Register all our translated fields for models here.
"""

from modeltranslation.translator import translator, TranslationOptions

from .models import Project


class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'features', 'region', 'locality')

translator.register(Project, ProjectTranslationOptions)