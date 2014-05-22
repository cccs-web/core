from django.contrib import admin

import cvs.models as cm


class CVAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'telephone']

admin.site.register(cm.CV, CVAdmin)
