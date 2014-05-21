from django.contrib import admin
from django.utils.safestring import mark_safe

import cvs.models as cm


class HasProjectsAdmin(admin.ModelAdmin):

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        extra_context['projects'] = list(obj.projects.all())
        return super(HasProjectsAdmin, self).change_view(request, object_id, form_url, extra_context)


class CountryAdmin(HasProjectsAdmin):
    list_display = ('name', 'iso_english_name', 'fips', 'iso_numeric', 'iso_3166', 'iso', 'project_count', 'notes')

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
        return mark_safe(u'<a href="{u}">{name}</a>'.format(u=instance.admin_url, name=instance.name))

    readonly_fields = ('project_name',)

    def has_delete_permission(self, request, obj=None):
        return False


class CCCSSubThemeAdmin(HasProjectsAdmin):
    list_display = ('name', 'theme', 'project_count')
    inlines = [ProjectInline]

admin.site.register(cm.CCCSSubTheme, CCCSSubThemeAdmin)


class CCCSSubThemeInline(admin.TabularInline):
    model = cm.CCCSSubTheme
    list_display = ['name', 'project_count']
    extra = 1


class CCCSThemeAdmin(HasProjectsAdmin):
    list_display = ['name', 'project_count']
    inlines = [
        CCCSSubThemeInline]

admin.site.register(cm.CCCSTheme, CCCSThemeAdmin)


class CCCSSubSectorAdmin(HasProjectsAdmin):
    list_display = ('name', 'sector', 'project_count')
    inlines = [ProjectInline]

admin.site.register(cm.CCCSSubSector, CCCSSubSectorAdmin)


class CCCSSubSectorInline(admin.TabularInline):
    model = cm.CCCSSubSector
    list_display = ['name']
    extra = 1


class CCCSSectorAdmin(HasProjectsAdmin):
    list_display = ['name', 'project_count']
    inlines = [
        CCCSSubSectorInline]

admin.site.register(cm.CCCSSector, CCCSSectorAdmin)


class IFCSubThemeInline(admin.TabularInline):
    model = cm.IFCSubTheme
    extra = 1


class IFCThemeAdmin(HasProjectsAdmin):
    list_display = ['name', 'project_count']
    inlines = [
        IFCSubThemeInline]

admin.site.register(cm.IFCTheme, IFCThemeAdmin)


class IFCSubThemeAdmin(HasProjectsAdmin):
    list_display = ('name', 'theme', 'project_count')
    inlines = [ProjectInline]

admin.site.register(cm.IFCSubTheme, IFCSubThemeAdmin)


class IFCSectorAdmin(HasProjectsAdmin):
    list_display = ['name', 'project_count']

admin.site.register(cm.IFCSector, IFCSectorAdmin)


class CVAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'telephone']

admin.site.register(cm.CV, CVAdmin)