from django.contrib.gis import admin

from models import Village


class VillageAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'population', 'provinsi', 'kecamatan', 'desa', 'quartile')
    list_filter = ('provinsi', 'kecamatan', 'desa')

admin.site.register(Village, VillageAdmin)
