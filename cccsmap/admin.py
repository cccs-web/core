from django.contrib.gis import admin

from models import Village


class VillageAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'population', 'provinsi', 'kecamatan', 'desa', 'quartile')

admin.site.register(Village, VillageAdmin)
