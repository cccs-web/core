from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

import cvs.models as cm


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_english_name', 'fips', 'iso_numeric', 'iso_3166', 'iso', 'notes')

admin.site.register(cm.Country, CountryAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_range', 'locality', 'region')

admin.site.register(cm.Project, ProjectAdmin)


class ProjectInline(admin.TabularInline):
    model = cm.Project
    extra = 0

    def __init__(self, parent_model, admin_site):
        super(ProjectInline, self).__init__(parent_model, admin_site)
        self.exclude = self.model._meta.get_all_field_names()


    def project_name(self, instance):
        url = reverse('admin:{0}_{1}_change'.format(
            instance._meta.app_label,  instance._meta.module_name),  args=[instance.id])
        return mark_safe(u'<a href="{u}">{name}</a>'.format(u=url, name=instance.name))

    readonly_fields = ('project_name',)

    def has_delete_permission(self, request, obj=None):
        return False


class CCCSSubThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'project_count')
    inlines = [ProjectInline]

admin.site.register(cm.CCCSSubTheme, CCCSSubThemeAdmin)


class CCCSSubThemeInline(admin.TabularInline):
    model = cm.CCCSSubTheme
    list_display = ['name', 'project_count']
    extra = 1


class CCCSThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_count']
    inlines = [
        CCCSSubThemeInline]

admin.site.register(cm.CCCSTheme, CCCSThemeAdmin)


class IFCSubThemeInline(admin.TabularInline):
    model = cm.IFCSubTheme
    extra = 1


class IFCThemeAdmin(admin.ModelAdmin):
    inlines = [
        IFCSubThemeInline]

admin.site.register(cm.IFCTheme, IFCThemeAdmin)


class IFCSectorAdmin(admin.ModelAdmin):
    pass

admin.site.register(cm.IFCSector, IFCSectorAdmin)