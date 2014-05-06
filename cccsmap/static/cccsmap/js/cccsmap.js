// POC Lots of work needed here - drawn from open layers geojson example

var lon = 131.114123;
var lat = -7.628902;
var zoom = 8;
var map, layer;

$(document).ready(function(){
    map = new OpenLayers.Map( 'map' );
    layer = new OpenLayers.Layer.WMS( "OpenLayers WMS",
        "http://vmap0.tiles.osgeo.org/wms/vmap0",
        {layers: 'basic'} );
    map.addLayer(layer);
    map.setCenter(new OpenLayers.LonLat(lon, lat), zoom);

    var vector_layer = new OpenLayers.Layer.Vector();
    map.addLayer(vector_layer);

    OpenLayers.Request.GET({
        url: "/maps/villages/",
        headers: {'Accept': 'application/json'},
        success: function(req){
            var g = new OpenLayers.Format.GeoJSON();
            var feature_collection = g.read(req.responseText);
            vector_layer.destroyFeatures();
            vector_layer.addFeatures(feature_collection);
        }
    })})
