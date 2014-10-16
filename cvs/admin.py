from django.contrib import admin

import cvs.models as cm


class CCCSRoleAdmin(admin.ModelAdmin):
    fields = ('name_en', 'name_fr', 'name_ru')

admin.site.register(cm.CCCSRole, CCCSRoleAdmin)


class CVProjectInline(admin.StackedInline):
    model = cm.CVProject
    extra = 1
    fields = ('project',
              'subproject',
              'from_date',
              'to_date',
              'position',
              'activities',
              'references',
              'client_beneficiary',
              'client_contract',
              'client_end',
              'contract')
    ordering = ['from_date']


class CVEducationInline(admin.TabularInline):
    model = cm.CVEducation
    extra = 1
    fields = ('from_date',
              'to_date',
              'institution',
              'qualification',
              'subject',
              'minors',)
    ordering = ['from_date']


class CVTrainingInline(admin.TabularInline):
    model = cm.CVTraining
    extra = 1
    ordering = ['from_date']


class CVMembershipInline(admin.TabularInline):
    model = cm.CVMembership
    extra = 1
    ordering = ['from_date']


class CVLanguageInline(admin.TabularInline):
    model = cm.CVLanguage
    extra = 1


class CVEmploymentInline(admin.StackedInline):
    model = cm.CVEmployment
    extra = 1
    ordering = ['from_date']


class CVPublicationInline(admin.TabularInline):
    model = cm.CVPublication
    extra = 1
    ordering = ['publication_date']


class CVAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'telephone']
    inlines = [CVProjectInline,
               CVEducationInline,
               CVTrainingInline,
               CVMembershipInline,
               CVLanguageInline,
               CVEmploymentInline,
               CVPublicationInline]
    fieldsets = ((None, {'fields': ('user',
                                    'status',
                                    'middle_names',
                                    'alternate_names',
                                    'content_en',
                                    'content_fr',
                                    'content_ru',
                                    'telephone',
                                    ('citizenship',
                                     'birth_country'),
                                    ('dob',
                                     'gender'),
                                    ('marital_status',
                                     'cccs_role'))}),
                 ('Address', {'classes': ('collapse-closed',),
                              'fields': ('street',
                                         'city',
                                         'state',
                                         'zip',
                                         'country')}),
                 ('Metadata', {'classes': ('collapse-closed',),
                               'fields': ('_meta_title',
                                          'slug',
                                          'short_url',
                                          'description',
                                          'gen_description',
                                          'keywords',
                                          'publish_date',
                                          'expiry_date')}))

    def first_name(self, obj):
        return obj.first_name

    first_name.admin_order_field = 'user__first_name'

    def last_name(self, obj):
        return obj.last_name

    last_name.admin_order_field = 'user__last_name'

    def email(self, obj):
        return obj.email

    email.admin_order_field = 'user__email'


admin.site.register(cm.CV, CVAdmin)
