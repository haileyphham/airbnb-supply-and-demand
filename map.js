
var map = L.map('map').setView([42.3601, -71.0589], 12); 


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//random 100 locations
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; 
    }
}


d3.csv('simplified_listings.csv').then(function(data) {
    shuffle(data);
    const sampleData = data.slice(0, 100);

    sampleData.forEach(function(d) {
        var lat = parseFloat(d.latitude);
        var lon = parseFloat(d.longitude);
        
        if (!isNaN(lat) && !isNaN(lon)) { 
        
            L.marker([lat, lon])
                .addTo(map)
                .bindPopup(`<strong>${d.name}</strong><br><a href="${d.listing_url}" target="_blank">View Listing</a>`);
        }
    });
}).catch(function(error) {
    console.error('Error loading CSV data:', error);
});
