var map = L.map('map', {"zoomControl": false}).setView([36.372, 127.363], 16);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.Control.setPosition('topright').addTo(map);

var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);

function submitForm(event) {
    event.preventDefault();

    map.remove();
    
    const startInput = document.getElementById('start');
    const destinationInput = document.getElementById('destination');

    const start = startInput.value;
    const destination = destinationInput.value;
    const apiKey = '5b3ce3597851110001cf624891534cea984549f89a12be1a922aa7bd';
    const apiUrl = `https://api.openrouteservice.org/v2/directions/foot-walking?api_key=${apiKey}&start=${start}&end=${destination}`;

    var start_parts = start.split(',');
    var end_parts = destination.split(',');
    const start_lat = parseFloat(start_parts[0]) + 0.00005;
    const start_lon = parseFloat(start_parts[1]) + 0.0005;
    const end_lat = parseFloat(end_parts[0]) + 0.0005;
    const end_lon = parseFloat(end_parts[1]) + 0.0005;

    var start_point = L.latLng(start_lon, start_lat);
    var end_point = L.latLng(end_lon, end_lat);

    var bounds = L.latLngBounds([start_point,end_point]);
    console.log(bounds);
    map = L.map('map', {"zoomControl": false});
    map.fitBounds(bounds);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    var start_marker = L.marker(start_point).addTo(map);
    var end_marker = L.marker(end_point).addTo(map);

    axios.get(apiUrl)
    .then(response => {
        console.log(response);
        const features = response.data.features.map(feature => ({
            type: "LineString",
            coordinates: feature.geometry.coordinates
        }));
        L.geoJSON(features).addTo(map);
        console.log(features);
    })
    .catch(error => {
        console.error(error);
    });
}