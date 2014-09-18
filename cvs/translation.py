"""
Register all our translated fields for models here.
"""

from modeltranslation.translator import translator, TranslationOptions
from projects.translation import UniqueNamedTranslationOptions

import cvs.models as cm


translator.register(cm.CCCSRole, UniqueNamedTranslationOptions)
translator.register(cm.Language, UniqueNamedTranslationOptions)


class CVTranslationOptions(TranslationOptions):
    fields = ('content',)

translator.register(cm.CV, CVTranslationOptions)