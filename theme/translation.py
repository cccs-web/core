"""
Register all translated fields for models in other modules here.
"""

from modeltranslation.translator import translator, TranslationOptions

from mezzanine_slides.models import Slide


class SlideTranslationOptions(TranslationOptions):
    fields = ('description', 'caption')

translator.register(Slide, SlideTranslationOptions)