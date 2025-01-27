// map.js

// Function to load the CSV data and plot markers
function loadCSV() {
    Papa.parse('listings.csv', {
        download: true,
        header: true, // Treats the first row as header
        dynamicTyping: true,
        complete: function(results) {
            // Initialize the map
            var map = L.map('map').setView([42.3601, -71.0589], 13); // Center map on Boston
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            // Loop through each row of the CSV and plot markers
            results.data.forEach(function(row) {
                // Clean data: Check if latitude and longitude are valid
                if (row.latitude && row.longitude && !isNaN(row.latitude) && !isNaN(row.longitude)) {
                    // Create a marker for each valid entry
                    L.marker([row.latitude, row.longitude])
                        .addTo(map)
                        .bindPopup("<b>" + row.name + "</b><br>Latitude: " + row.latitude + "<br>Longitude: " + row.longitude);
                }
            });
        }
    });
}

// Call the function to load CSV and render map
loadCSV();
