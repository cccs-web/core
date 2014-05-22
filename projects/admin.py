from django.contrib import admin
from django.utils.safestring import mark_safe

import projects.models as pm


class HasProjectsAdmin(admin.ModelAdmin):

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        extra_context['projects'] = list(obj.projects.all())
        return super(HasProjectsAdmin, self).change_view(request, object_id, form_url, extra_context)


class CountryAdmin(HasProjectsAdmin):
    list_display = ('name', 'iso_english_name', 'fips', 'iso_numeric', 'iso_3166', 'iso', 'project_count', 'notes')

admin.site.register(pm.Country, CountryAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_range', 'locality', 'region')


admin.site.register(pm.Project, ProjectAdmin)


class ProjectInline(admin.TabularInline):
    model = pm.Project
    extra = 0

    def __init__(self, parent_model, admin_site):
        super(ProjectInline, self).__init__(parent_model, admin_site)
        self.exclude = self.model._meta.get_all_field_names()


    def project_name(self, instance):
        return mark_safe(u'<a href="{u}">{name}</a>'.format(u=instance.admin_url, name=instance.name))

    readonly_fields = ('project_name',)

    def has_delete_permission(self, request, obj=None):
        return False


class CCCSSubThemeAdmin(HasProjectsAdmin):
    list_display = ('name', 'theme', 'project_count')
    inlines = [ProjectInline]

admin.site.register(pm.CCCSSubTheme, CCCSSubThemeAdmin)


class CCCSSubThemeInline(admin.TabularInline):
    model = pm.CCCSSubTheme
    list_display = ['name', 'project_count']
    extra = 1


class CCCSThemeAdmin(HasProjectsAdmin):
    list_display = ['name', 'project_count']
    inlines = [
        CCCSSubThemeInline]

admin.site.register(pm.CCCSTheme, CCCSThemeAdmin)


class CCCSSubSectorAdmin(HasProjectsAdmin):
    list_display = ('name', 'sector', 'project_count')
    inlines = [ProjectInline]

admin.site.register(pm.CCCSSubSector, CCCSSubSectorAdmin)


class CCCSSubSectorInline(admin.TabularInline):
    model = pm.CCCSSubSector
    list_display = ['name']
    extra = 1


class CCCSSectorAdmin(HasProjectsAdmin):
    list_display = ['name', 'project_count']
    inlines = [
        CCCSSubSectorInline]

admin.site.register(pm.CCCSSector, CCCSSectorAdmin)


class IFCSubThemeInline(admin.TabularInline):
    model = pm.IFCSubTheme
    extra = 1


class IFCThemeAdmin(HasProjectsAdmin):
    list_display = ['name', 'project_count']
    inlines = [
        IFCSubThemeInline]

admin.site.register(pm.IFCTheme, IFCThemeAdmin)


class IFCSubThemeAdmin(HasProjectsAdmin):
    list_display = ('name', 'theme', 'project_count')
    inlines = [ProjectInline]

admin.site.register(pm.IFCSubTheme, IFCSubThemeAdmin)


class IFCSectorAdmin(HasProjectsAdmin):
    list_display = ['name', 'project_count']

admin.site.register(pm.IFCSector, IFCSectorAdmin)

