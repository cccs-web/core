# https://docs.djangoproject.com/en/1.6/ref/contrib/gis/tutorial/
# poc work - will need refactoring
"""
Import the Villages_GE.shp fileset as Village model objects.
"""
import os
from django.contrib.gis.utils import LayerMapping
from models import Village, village_mapping

pwd = os.path.dirname(__file__)
villages_shp = os.path.abspath(os.path.join(pwd, 'shapefiles/villages/Villages_GE.shp'))


def run(verbose=True):
    lm = LayerMapping(Village, villages_shp, village_mapping, transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)


