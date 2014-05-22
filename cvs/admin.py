from django.contrib import admin

import cvs.models as cm


class CVProjectInline(admin.TabularInline):
    model = cm.CVProject


class CVAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'telephone']
    inlines = [CVProjectInline]

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
