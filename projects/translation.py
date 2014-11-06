"""
Register all our translated fields for models here.
"""

from modeltranslation.translator import translator, TranslationOptions

import projects.models as pm


class UniqueNamedTranslationOptions(TranslationOptions):
    fields = ('name', 'plural_name')

translator.register(pm.CCCSSector, UniqueNamedTranslationOptions)
translator.register(pm.IFCTheme, UniqueNamedTranslationOptions)
translator.register(pm.IFCSector, UniqueNamedTranslationOptions)
translator.register(pm.CCCSTheme, UniqueNamedTranslationOptions)


class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'region', 'locality')

translator.register(pm.Project, ProjectTranslationOptions)