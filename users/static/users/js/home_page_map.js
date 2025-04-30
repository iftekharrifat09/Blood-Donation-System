// Initialize Leaflet map
var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Tracking user location
if (!navigator.geolocation) {
    console.log("Your browser doesn't support Geolocation Feature");
} else {
    setInterval(() => {
        navigator.geolocation.getCurrentPosition(getPosition);
    }, 3000);
}

var marker, circle;

function getPosition(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    var accuracy = position.coords.accuracy;

    // Remove previous marker and circle
    if (marker) map.removeLayer(marker);
    if (circle) map.removeLayer(circle);

    marker = L.marker([lat, lng]);
    circle = L.circle([lat, lng], { radius: accuracy });

    var featureGroup = L.featureGroup([marker, circle]).addTo(map);
    map.fitBounds(featureGroup.getBounds());

    console.log(`Your lat: ${lat}, lng: ${lng}, accuracy: ${accuracy}`);
}

