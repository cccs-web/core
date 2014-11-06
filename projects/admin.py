from django.contrib import admin
from django.utils.safestring import mark_safe

import projects.models as pm
import cvs.models as cm


class HasProjectsAdmin(admin.ModelAdmin):

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        extra_context['projects'] = list(obj.projects.all())
        return super(HasProjectsAdmin, self).change_view(request, object_id, form_url, extra_context)


class CountryAdmin(HasProjectsAdmin):
    list_display = ('name', 'iso_english_name', 'fips', 'iso_numeric', 'iso_3166', 'iso', 'project_count', 'notes')

admin.site.register(pm.Country, CountryAdmin)


class CVProjectInline(admin.StackedInline):
    extra = 1
    model = cm.CVProject
    exclude = ('cv',)
    readonly_fields = ('cv_link',)
    fields = ('subproject',
              'from_date',
              'to_date',
              'position',
              'activities',
              'references',
              'client_beneficiary',
              'client_contract',
              'client_end',
              'contract',
              'cv_link')

    def cv_link(self, instance):
        return mark_safe(u'<a href="{u}">{name}</a>'.format(u=instance.cv.admin_url, name=instance.cv.title))


class SubProjectInline(admin.TabularInline):
    extra = 1
    model = pm.SubProject
    fields = ('name',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_date', 'to_date', 'locality', 'region')
    list_filter = ('countries', 'to_date')
    search_fields = ('title', 'region')
    filter_horizontal = ('countries', 'cccs_subthemes', 'cccs_subsectors', 'ifc_subthemes', 'ifc_sectors')
    inlines = (CVProjectInline, SubProjectInline)
    fieldsets = ((None, {'fields': ('title_en',
                                    'title_fr',
                                    'title_ru',
                                    'status',
                                    'content_en',
                                    'content_fr',
                                    'content_ru',
                                    'owner',
                                    'sponsor',
                                    'from_date',
                                    'to_date',
                                    'loan_or_grant')}),
                 ('Location', {'classes': ('collapse-closed',),
                               'fields': ('countries',
                                          'region_en',
                                          'region_fr',
                                          'region_ru',
                                          'locality_en',
                                          'locality_fr',
                                          'locality_ru')}),
                 ('Categorization', {'classes': ('collapse-closed',),
                                     'fields': ('cccs_subthemes',
                                     'cccs_subsectors',
                                     'ifc_subthemes',
                                     'ifc_sectors',
                                     'tags')}),
                 ('Metadata', {'classes': ('collapse-closed',),
                               'fields': ('_meta_title',
                                          'slug',
                                          'short_url',
                                          'keywords',
                                          'publish_date',
                                          'expiry_date')}))

    def name(self, instance):
        return getattr(instance, 'name')
    name.admin_order_field = 'title'


admin.site.register(pm.Project, ProjectAdmin)


class ProjectInline(admin.TabularInline):
    extra = 0

    def __init__(self, parent_model, admin_site):
        super(ProjectInline, self).__init__(parent_model, admin_site)
        self.exclude = self.model._meta.get_all_field_names()


    def project_name(self, instance):
        return mark_safe(u'<a href="{u}">{name}</a>'.format(u=instance.project.admin_url, name=instance.project.name))

    readonly_fields = ('project_name',)

    def has_delete_permission(self, request, obj=None):
        return False


class ProjectCCCSSubThemeInline(ProjectInline):
    model = pm.Project.cccs_subthemes.through


class ProjectCCCSSubSectorInline(ProjectInline):
    model = pm.Project.cccs_subsectors.through


class ProjectIFCSubThemeInline(ProjectInline):
    model = pm.Project.ifc_subthemes.through


class CCCSSubThemeAdmin(HasProjectsAdmin):
    list_display = ('name', 'theme', 'project_count')
    inlines = [ProjectCCCSSubThemeInline]

admin.site.register(pm.CCCSSubTheme, CCCSSubThemeAdmin)


class CCCSSubThemeInline(admin.TabularInline):
    model = pm.CCCSSubTheme
    extra = 1

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(CCCSSubThemeInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name':
            field.widget.attrs['style'] = 'width: 64em;'
        return field


class CCCSThemeAdmin(HasProjectsAdmin):
    list_display = ['name', 'abbreviation', 'project_count']
    inlines = [
        CCCSSubThemeInline]

admin.site.register(pm.CCCSTheme, CCCSThemeAdmin)


class CCCSSubSectorAdmin(HasProjectsAdmin):
    list_display = ('name', 'sector', 'project_count')
    inlines = [ProjectCCCSSubSectorInline]

admin.site.register(pm.CCCSSubSector, CCCSSubSectorAdmin)


class CCCSSubSectorInline(admin.TabularInline):
    model = pm.CCCSSubSector
    list_display = ['name']
    extra = 1


class CCCSSectorAdmin(HasProjectsAdmin):
    list_display = ['name', 'abbreviation', 'project_count']
    inlines = [
        CCCSSubSectorInline]

admin.site.register(pm.CCCSSector, CCCSSectorAdmin)


class IFCSubThemeInline(admin.TabularInline):
    model = pm.IFCSubTheme
    extra = 1


class IFCThemeAdmin(HasProjectsAdmin):
    list_display = ['name', 'abbreviation', 'project_count']
    inlines = [
        IFCSubThemeInline]

admin.site.register(pm.IFCTheme, IFCThemeAdmin)


class IFCSubThemeAdmin(HasProjectsAdmin):
    list_display = ('name', 'theme', 'project_count')
    inlines = [ProjectIFCSubThemeInline]

admin.site.register(pm.IFCSubTheme, IFCSubThemeAdmin)


class IFCSectorAdmin(HasProjectsAdmin):
    list_display = ['name', 'project_count']

admin.site.register(pm.IFCSector, IFCSectorAdmin)


class SubProjectAdmin(admin.ModelAdmin):
    list_display = ('project', 'name')
    list_filter = ('project',)
    search_fields = ('project__name', 'name')

admin.site.register(pm.SubProject, SubProjectAdmin)

