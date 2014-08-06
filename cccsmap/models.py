# This is an auto-generated Django model module created by ogrinspect.
# ~$ django ogrinspect Villages_GE.shp Village --srid=4326 --mapping
from django.contrib.gis.db import models


class Village(models.Model):
    name = models.CharField(max_length=250)
    population = models.FloatField()
    provinsi = models.CharField(max_length=40)
    kecamatan = models.CharField(max_length=40)
    desa = models.CharField(max_length=40)
    quartile = models.CharField(max_length=50)
    dataseries = models.CharField(max_length=150)
    geom = models.PointField(srid=4326)
    objects = models.GeoManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


# Auto-generated `LayerMapping` dictionary for Village model
village_mapping = {
    'name': 'name',
    'population': 'population',
    'provinsi': 'PROVINSI',
    'kecamatan': 'KECAMATAN',
    'desa': 'DESA',
    'quartile': 'Quartile',
    'dataseries': 'DataSeries',
    'geom': 'POINT',
}

