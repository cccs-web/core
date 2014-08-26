from django.contrib import admin

import cvs.models as cm

admin.site.register(cm.AssociateRole, admin.ModelAdmin)


class CVProjectInline(admin.StackedInline):
    model = cm.CVProject
    extra = 1


class CVEducationInline(admin.TabularInline):
    model = cm.CVEducation
    extra = 1


class CVTrainingInline(admin.TabularInline):
    model = cm.CVTraining
    extra = 1


class CVMembershipInline(admin.TabularInline):
    model = cm.CVMembership
    extra = 1


class CVLanguageInline(admin.TabularInline):
    model = cm.CVLanguage
    extra = 1


class CVEmploymentInline(admin.StackedInline):
    model = cm.CVEmployment
    extra = 1


class CVPublicationInline(admin.TabularInline):
    model = cm.CVPublication
    extra = 1


class CVAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'telephone']
    inlines = [CVProjectInline,
               CVEducationInline,
               CVTrainingInline,
               CVMembershipInline,
               CVLanguageInline,
               CVEmploymentInline,
               CVPublicationInline]

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
