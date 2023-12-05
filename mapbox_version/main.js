// main.js
import { mapboxAccessToken } from './config.js';

mapboxgl.accessToken = mapboxAccessToken;

const map = new mapboxgl.Map({
    container: 'map', // container ID
    center: [-123.115540, 49.280747], // starting position [lng, lat]
    zoom: 12 // starting zoom
});

// Create a default Marker and add it to the map.
const marker_neu = new mapboxgl.Marker({ color: 'red' })
    .setLngLat([-123.115540, 49.280747])
    .addTo(map);

// Create click map event
let selectedPoints = [];

map.on('click', function(e) {
  const coordinates = e.lngLat;
  new mapboxgl.Popup()
      .setLngLat(coordinates)
      .setHTML("<button onclick='addLocation(" + JSON.stringify(coordinates) + ")'>Add this location</button>")
      .addTo(map);
});

window.addLocation = function(coordinates) {
  if (selectedPoints.length < 5) {
    selectedPoints.push(coordinates);
    new mapboxgl.Marker().setLngLat(coordinates).addTo(map);
  } else {
    alert("You can select up to 5 locations.");
  }
}

// Create search bar
// Add geocoder control to the map
map.addControl(
    new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl
    })
    );