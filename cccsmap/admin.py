from django.contrib.gis import admin

from models import Village

admin.site.register(Village, admin.OSMGeoAdmin)
