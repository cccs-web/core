from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

import projects.models as pm
import cvs.models as cm
from django.db.models import signals

class HasProjectsAdmin(admin.ModelAdmin):

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        extra_context['projects'] = list(obj.projects.all())
        return super(HasProjectsAdmin, self).change_view(request, object_id, form_url, extra_context)


class CountryAdmin(HasProjectsAdmin):
    list_display = ('name', 'iso_english_name', 'fips', 'iso_numeric', 'iso_3166', 'iso', 'project_count', 'notes')

admin.site.register(pm.Country, CountryAdmin)

class CVProjectProxy(cm.CVProject):
    class Meta:
        proxy = True

    def __unicode__(self):
        return self.cv.full_name

signals.post_save.connect(cm.cv_project_post_save, sender=CVProjectProxy)


class CVProjectInline(admin.StackedInline):
    extra = 1
    model = CVProjectProxy
    verbose_name = "CV"
    verbose_name_plural = "Associated CV Data"
    fields = (
              'from_date',
              'to_date',
              'position',
              'activities',
              'references',
              'client_beneficiary',
              'client_contract',
              'client_end',
              'contract',
              'cv')

    def has_add_permission(self, request):
        return False

class ProjectProxy(pm.Project):
    class Meta:
        proxy = True

    @property
    def name(self):
        pre = ''
        if self.parent:
            pre = '---'
        return pre + self.title

class ProjectForm(forms.ModelForm):
    class Meta:
        model = pm.Project

    def clean(self):
        super(ProjectForm, self).clean()
        cleaned_data = self.cleaned_data

        if not cleaned_data.get('parent'):
            self.instance.cccs_subthemes = cleaned_data['cccs_subthemes']
            self.instance.cccs_subsectors = cleaned_data['cccs_subsectors']
            self.instance.ifc_subthemes = cleaned_data['ifc_subthemes']
            self.instance.ifc_sectors = cleaned_data['ifc_sectors']
            self.instance.full_clean()

        return cleaned_data


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    readonly_fields = ('Super_sub_project_relation', 'id')
    list_display = ('name', 'from_date', 'to_date', 'locality', 'region')
    list_filter = ('countries', 'to_date')
    search_fields = ('title', 'region')
    filter_horizontal = ('countries', 'cccs_subthemes', 'cccs_subsectors', 'ifc_subthemes', 'ifc_sectors')
    inlines = (CVProjectInline, )
    fieldsets = ((None, {'fields': (
                                    'parent',
                                    'Super_sub_project_relation',
                                    'title_en',
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
                                    'loan_or_grant',
                                #    'features_en',
                                #    'features_fr',
                                #    'features_ru'
                        )}),
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
                               'fields': ('slug',
                                          'short_url',
                                          'keywords',
                                          'publish_date',
                                          'expiry_date')}))


    def Super_sub_project_relation(self, instance):
        html = "Super Project:   <a href='%s'>%s</a>" % (instance.parent.admin_url, instance.parent.title) if instance.parent else ''
        html += ('<br>' if html else '')
        sub_projects = getattr(instance, 'sub_projects')
        links = []
        for c in sub_projects:
            links.append("<a href='%s'>%s</a>" % (c.admin_url, c.title))

        html += ("Sub Project"+("s" if len(links) > 1 else '')+":  " + ",".join(links) if len(links) > 0 else '')
        return html

    Super_sub_project_relation.allow_tags = True
    Super_sub_project_relation.short_description = 'Super/Sub project relation'
    def name(self, instance):
        return getattr(instance, 'name')
    name.admin_order_field = 'title'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs["queryset"] = pm.Project.objects.filter(parent=None)
        return super(ProjectAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ProjectProxy, ProjectAdmin)


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


