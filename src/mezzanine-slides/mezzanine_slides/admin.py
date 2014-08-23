from django.conf import settings

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin
from mezzanine.forms.admin import FormAdmin
from mezzanine.galleries.admin import GalleryAdmin

from .models import Slide


class SlideInline(TabularDynamicInlineAdmin):
    model = Slide

admin_classes_with_slides = [PageAdmin, FormAdmin, GalleryAdmin]

if "cartridge.shop" in settings.INSTALLED_APPS:
    from cartridge.shop.admin import CategoryAdmin
    admin_classes_with_slides.append(CategoryAdmin)

for admin_class in admin_classes_with_slides:
    setattr(admin_class, 'inlines', list(admin_class.inlines) + [SlideInline])



