// main.js
import { mapboxAccessToken } from './config.js';

mapboxgl.accessToken = mapboxAccessToken;

const map = new mapboxgl.Map({
    container: 'map', // container ID
    center: [-123.115540, 49.280747], // starting position [lng, lat]
    zoom: 12 // starting zoom
});

// Create a default Marker and add it to the map.
const marker1 = new mapboxgl.Marker({color:'red'})
    .setLngLat([-123.115540, 49.280747])
    .addTo(map);