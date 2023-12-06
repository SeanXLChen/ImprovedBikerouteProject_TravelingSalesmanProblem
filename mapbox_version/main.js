// main.js
import { mapboxAccessToken } from './config.js';

mapboxgl.accessToken = mapboxAccessToken;

const map = new mapboxgl.Map({
    container: 'map', // container ID
    center: [-123.115540, 49.280747], // starting position [lng, lat]
    zoom: 12 // starting zoom
});

const marker_neu = new mapboxgl.Marker({ color: 'red' })
    .setLngLat([-123.115540, 49.280747])
    .addTo(map);

let selectedPoints = [
    [-123.115540, 49.280747], // NEU Campus coordinates
];

let fullRoute = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "LineString",
        "coordinates": []
    }
};

map.on('click', function (e) {
    const coordinates = e.lngLat.toArray(); // Convert to array format
    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML("<button onclick='addLocation(" + JSON.stringify(coordinates) + ")'>Add this location</button>")
        .addTo(map);
});

window.addLocation = function (coordinates) {
    if (selectedPoints.length < 6) {
        selectedPoints.push(coordinates);
        new mapboxgl.Marker().setLngLat(coordinates).addTo(map);
    } else {
        alert("You can select up to 6 locations.");
    }
}

const geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl
});

map.addControl(geocoder);

geocoder.on('result', function (e) {
    const coordinates = e.result.geometry.coordinates;
    const popupHTML = "<button onclick='addLocation(" + JSON.stringify(coordinates) + ")'>Add this location</button>";
    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(popupHTML)
        .addTo(map);
});

class CalculateRouteControl {
    onAdd(map) {
        this.map = map;
        this.container = document.createElement('div');
        this.container.className = 'mapboxgl-ctrl';
        const button = document.createElement('button');
        button.textContent = 'Calculate Route';

        button.addEventListener('click', async function () {
            if (selectedPoints.length < 3) {
                alert("Please select at least 2 locations.");
                return;
            }
            
            // Add the starting point (NEU Campus) to the end of the points to form a loop
            selectedPoints.push(selectedPoints[0]);
            let coordinatesString = selectedPoints.map(coord => coord.join(',')).join(';');
            let profile = 'mapbox/cycling'; // This is your profile for routing
            let mapboxApiUrl = `https://api.mapbox.com/directions-matrix/v1/${profile}/${coordinatesString}?access_token=${mapboxAccessToken}&annotations=duration,distance`;

            try {
                const response = await fetch(mapboxApiUrl);
                const data = await response.json();
                if (data.code === 'Ok') {
                    console.log('Matrix API response:', data);
                    const tspPath = heldKarpWithPath(data.distances);
                    await drawFullRoute(tspPath.path, selectedPoints);
                    fitMapToBounds(fullRoute);
                } else {
                    console.error('Error fetching Matrix API:', data.code, data.message);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });

        this.container.appendChild(button);
        return this.container;
    }

    onRemove() {
        this.container.parentNode.removeChild(this.container);
        this.map = undefined;
    }
}

map.addControl(new CalculateRouteControl(), 'top-right');


// Held-Karp Algorithm
function heldKarpWithPath(distances) {
    const n = distances.length;
    const VISITED_ALL = (1 << n) - 1;
    let memo = Array.from({ length: n }, () => Array(VISITED_ALL).fill(Infinity));
    let nextCity = Array.from({ length: n }, () => Array(VISITED_ALL).fill(null));

    function visit(city, visited) {
        if (visited === VISITED_ALL) {
            return [distances[city][0], 0];
        }
        if (memo[city][visited] !== Infinity) {
            return [memo[city][visited], null];
        }

        for (let next = 0; next < n; next++) {
            if ((visited & (1 << next)) === 0) {
                const [tempDistance] = visit(next, visited | (1 << next));
                const newDistance = distances[city][next] + tempDistance;
                if (newDistance < memo[city][visited]) {
                    memo[city][visited] = newDistance;
                    nextCity[city][visited] = next;
                }
            }
        }
        return [memo[city][visited], null];
    }

    function findPath(city, visited) {
        if (visited === VISITED_ALL) {
            return [city];
        }
        const next = nextCity[city][visited];
        return [city, ...findPath(next, visited | (1 << next))];
    }

    const [shortestDistance] = visit(0, 1); // Start at city 0
    const path = findPath(0, 1);

    return { shortestDistance, path };
}

// // Example usage:
// const matrix = [
//     [0, 616.3, 763.2, 560.7, 673.7],
//     [725.2, 0, 620.4, 1054.1, 622.6],
//     [935.5, 695.1, 0, 587.3, 184],
//     [694.1, 1165.8, 673.2, 0, 550.7],
//     [836.8, 733.6, 161.8, 517.2, 0]
// ];

// const { shortestDistance, path } = heldKarpWithPath(matrix);
// console.log('Shortest path distance:', shortestDistance);
// console.log('Path:', path.join(' -> '));

// Define a function to make an API call for the directions between two points
function getDirections(start, end, profile = 'mapbox/cycling') {
    const url = `https://api.mapbox.com/directions/v5/${profile}/${start.join(',')};${end.join(',')}` +
        `?geometries=geojson&access_token=${mapboxAccessToken}`;

    return fetch(url).then(response => response.json());
}

async function drawFullRoute(path, locations) {
    fullRoute.geometry.coordinates = [];

    for (let i = 0; i < path.length - 1; i++) {
        const start = locations[path[i]];
        const end = locations[path[i + 1]];

        if (!start || !end) {
            console.error('Undefined start or end in path:', start, end);
            continue;
        }

        const response = await getDirections(start, end);
        if (response.routes && response.routes.length) {
            const routeCoordinates = response.routes[0].geometry.coordinates;
            fullRoute.geometry.coordinates.push(...routeCoordinates);
        }
    }

    if (fullRoute.geometry.coordinates.length > 0) {
        if (map.getSource('full-route')) {
            map.getSource('full-route').setData(fullRoute);
        } else {
            map.addSource('full-route', {
                "type": "geojson",
                "data": fullRoute,
                "lineMetrics": true // Enable line metrics for gradient lines
            });

            map.addLayer({
                "id": "full-route",
                "type": "line",
                "source": "full-route",
                "layout": {
                    "line-join": "round",
                    "line-cap": "round"
                },
                "paint": {
                    "line-color": "#ff7e5f",
                    "line-width": 4,
                    // Add the gradient here
                    'line-gradient': [
                        'interpolate',
                        ['linear'],
                        ['line-progress'],
                        0, "#3f98eb", // Start color of the gradient (light blue)
                        1, "#00008B"  // End color of the gradient (dark blue)
                    ]
                }
            });
        }

        fitMapToBounds(fullRoute);
    } else {
        console.error('No route coordinates to draw.');
    }
}

function fitMapToBounds(route) {
    if (route.geometry.coordinates.length > 0) {
        const bounds = new mapboxgl.LngLatBounds();
        route.geometry.coordinates.forEach(coord => {
            bounds.extend(coord);
        });
        map.fitBounds(bounds, { padding: 20 });
    } else {
        console.error('Cannot fit map bounds: No coordinates in route.');
    }
}
