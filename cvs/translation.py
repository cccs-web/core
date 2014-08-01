"""
Register all our translated fields for models here.
"""

from modeltranslation.translator import translator
from projects.translation import UniqueNamedTranslationOptions

import cvs.models as cm


translator.register(cm.AssociateRole, UniqueNamedTranslationOptions)
translator.register(cm.Language, UniqueNamedTranslationOptions)