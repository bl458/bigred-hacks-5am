var heatMapData;
var map;
var heatmap;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 42.4472051, lng: -76.48297680000002},
    zoom: 15
  });
  heatMapData = [
    <!--PSB-->
    {location: new google.maps.LatLng(42.4498226, -76.481841), weight: 0.5},
    <!--GATES-->
    {location: new google.maps.LatLng(42.4448765, -76.4808143), weight: 0.2}
  ];
  heatmap = new google.maps.visualization.HeatmapLayer({
            data: heatMapData,
            radius: 50
  });
  heatmap.setMap(map);
}
