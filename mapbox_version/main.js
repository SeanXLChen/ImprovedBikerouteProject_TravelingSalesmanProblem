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
let selectedPoints = [
    [-123.115540, 49.280747], // NEU Campus coordinates
];

map.on('click', function (e) {
    const coordinates = e.lngLat;
    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML("<button onclick='addLocation(" + JSON.stringify(coordinates) + ")'>Add this location</button>")
        .addTo(map);
});

window.addLocation = function (coordinates) {
    // Check if coordinates are in object format and convert them to array format
    if (typeof coordinates === 'object' && coordinates.hasOwnProperty('lng') && coordinates.hasOwnProperty('lat')) {
        coordinates = [coordinates.lng, coordinates.lat];
    }

    if (selectedPoints.length < 5) {
        selectedPoints.push(coordinates);
        new mapboxgl.Marker().setLngLat(coordinates).addTo(map);
        console.log(selectedPoints); // Log after adding a new point
    } else {
        alert("You can select up to 5 locations.");
    }
}

// Create search bar
// Add geocoder control to the map
const geocoder = new MapboxGeocoder({ // Create a Geocoder control
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl
});

map.addControl(geocoder); // Add Geocoder control to the map

// Listen for the 'result' event on the Geocoder
geocoder.on('result', function (e) {
    const coordinates = e.result.geometry.coordinates;

    // Create a Popup with a button for adding the location
    const popupHTML = "<button onclick='addLocation(" + JSON.stringify(coordinates) + ")'>Add this location</button>";
    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(popupHTML)
        .addTo(map);
});



// Prepare Data for Mapbox Matrix API 

// Add the button to the map
map.on('load', function () {
    // Create the button element
    const button = document.createElement('button');
    button.id = 'calculate-route';
    button.textContent = 'Calculate Route';

    // Add an event listener to the button
    button.addEventListener('click', function () {
        // Code to handle button click
    });

    // Append the button to the DOM
    document.body.appendChild(button); // Or append it to a specific element
});

class CalculateRouteControl {
    onAdd(map) {
        this.map = map;
        this.container = document.createElement('div');
        this.container.className = 'mapboxgl-ctrl';
        const button = document.createElement('button');
        button.textContent = 'Calculate Route';
        button.addEventListener('click', function () {
            // Code to handle button click
            let coordinatesString = selectedPoints.map(coord => coord.join(',')).join(';');
            let profile = 'mapbox/driving'; // Choose the appropriate profile
            let mapboxApiUrl = `https://api.mapbox.com/directions-matrix/v1/${profile}/${coordinatesString}?access_token=${mapboxAccessToken}&annotations=duration,distance`;

            fetch(mapboxApiUrl)
                .then(response => response.json())
                .then(data => {
                    if (data.code === 'Ok') {
                        console.log('Distance Matrix:', data.distances);
                        console.log('Duration Matrix:', data.durations);
                        // Further processing of the matrix data
                    } else {
                        console.error('Error fetching Matrix API:', data.code, data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
        this.container.appendChild(button);
        return this.container;
    }

    onRemove() {
        this.container.parentNode.removeChild(this.container);
        this.map = undefined;
    }
}

// Add the custom control to the map
map.addControl(new CalculateRouteControl(), 'top-right');