OpenLayers.ProxyHost = "http://vgr.salimalifoundation.org/gis/proxy?url=";
var map, infoControls;
var plots_gbl;
var bounds = new OpenLayers.Bounds(
		8483476,1154149,
		8484709,1153340
);
var labels = ["Id", "Survey No.", "Subdivision No.", "Rent Roll No.", "Owner",
    "Databank Survey No.", "Databank Rent Roll", "Databank Owner", "Databank Status",
    "Farming", "Lease", "Lessee", "Last Cultivated", "No Consent", "Threat", "Organic",
    "Heirloom seeds", "Fallow Block"];
function load(plots) {
	map = new OpenLayers.Map('map', {projection: new
	OpenLayers.Projection("EPSG:900913"), numZoomLevels: 28});
	plots_gbl=plots;

	var districts = new OpenLayers.Layer.WMS("Districts",
            "http://188.166.179.117:8080/geoserver-2.5/vayal/wms", 
            {'layers': 'vayal:districts', projection: new
            OpenLayers.Projection("EPSG:4326"), transparent: true, format: 'image/gif'},
            {isBaseLayer: false}
	);
        
	var kannoli = new OpenLayers.Layer.WMS("Kannolichira",
            "http://188.166.179.117:8080/geoserver-2.5/vgr/wms",
            {'layers': 'vgr:plots_modified', projection: new
            OpenLayers.Projection("EPSG:4326"), transparent: true, format:
            'image/gif'},
            {isBaseLayer: false}
	);
	
	var osm = new OpenLayers.Layer.OSM("OpenStreetMap");
	
	var ggle = new OpenLayers.Layer.Google(
	    "Google Hybrid",
	    {type: google.maps.MapTypeId.HYBRID, numZoomLevels: 20}
        );
        
        infoControls = new OpenLayers.Control.WMSGetFeatureInfo({
                url: 'http://188.166.179.117:8080/geoserver-2.5/vgr/wms', 
                title: 'Identify features by clicking',
                layers: [kannoli],
                queryVisible: true
            });
            
	infoControls.infoFormat = 'application/vnd.ogc.gml';
	infoControls.events.register("getfeatureinfo", this, showInfo);

        map.addLayers([osm, ggle, kannoli]); 
        map.addControl(infoControls); 
        map.addControl(new OpenLayers.Control.LayerSwitcher());
        infoControls.activate();
        map.zoomToExtent(bounds);
}

function showInfo(evt) {
        if (evt.features && evt.features.length) {
          var id = evt.features[0].attributes.id;
          var ind = id-1;
          var text = '<table>';
          for (var i=0; i<18; i++){
            text = text+'<tr>\
            <th><b>'+labels[i]+'</b></th>\
            <th>'+plots[ind][i]+'</th>\
            </tr>';
          }
          text = text+'</table><p></p>';
          document.getElementById('responseText').innerHTML = text;
        }
        else {
          document.getElementById('responseText').innerHTML = '';
        } 
}

    
            