from django.views.generic.list import ListView
from django.http import HttpResponse

from vectorformats.Formats import Django, GeoJSON

from models import Village


class VillageView(ListView):
    model = Village

    def get_queryset(self):
        """
        Just return them all for now
        """
        return super(VillageView, self).get_queryset()

    def render_to_response(self, context, **response_kwargs):
        """
        Return as a nice geojson layer
        """
        village_list = context['village_list']
        properties_wanted = ['name', 'population', 'provinsi', 'kecamatan', 'desa', 'quartile', 'dataseries']
        djf = Django.Django(geodjango="geom", properties=properties_wanted)
        encoder = GeoJSON.GeoJSON()
        geojson_str = encoder.encode(djf.decode(village_list))
        return HttpResponse(geojson_str, content_type="application/json")