// Function to fetch and send location data
function fetchAndSendLocation() {
    $('#loadingAnimation').removeClass('hidden');
    $('#contentContainer').addClass('hidden');

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error);
    } else {
        console.error("Geolocation is not supported by this browser.");
        showGeolocationPrompt();
    }

    async function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        try {
            // Reverse Geocoding with Nominatim API
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
            const data = await response.json();

            const city = data.address.city || data.address.town || data.address.village || "Unknown City";
            const state = data.address.state || "Unknown State";
            const pincode = data.address.postcode || "Unknown Pincode";

            // Update the HTML dynamically
            $('#weather_detail_header').text(city+" Weather");
            $('#city').text(city);
            $('#state').text(state);
            $('#pincode').text(pincode);

            // console.log(`City: ${city}, State: ${state}, Pincode: ${pincode}`);

            // Send the data to the backend via AJAX
            $.ajax({
                url: '/get_weather',
                method: 'GET',
                data: {
                    latitude: latitude,
                    longitude: longitude
                },
                success: function(response) {
                    console.log('Weather Data:', response.weather_data);
                    const weather = response.weather_data;

                    // Update weather details in the HTML
                    $('#city').text(weather.city || '-');
                    $('#temperature').text(weather.temperature || '-');
                    $('#precipitation').text(weather.precipitation || '-');
                    $('#humidity').text(weather.humidity || '-');
                    $('#wind_speed').text(weather.wind_speed || '-');
                    $('#description').text(weather.weather || '-');
                    if (weather.icon_url) {
                        $('#weather_icon').attr('src', weather.icon_url).removeClass('hidden');
                    }

                    // Update favicon and title
                    if (weather.img_src) {
                        $('#favicon').attr('href', weather.img_src);
                    }
                    document.getElementById('pageTitle').textContent = `${city}, ${state} Weather`;

                    // Hide loading animation and show content
                    $('#loadingAnimation').addClass('hidden');
                    $('#contentContainer').removeClass('hidden');
                },
                error: function(err) {
                    console.error('Error fetching weather data:', err);
                    $('#loadingAnimation').addClass('hidden');
                    $('#contentContainer').removeClass('hidden');
                }
            });
        } catch (err) {
            console.error("Error fetching location details:", err);
            $('#loadingAnimation').addClass('hidden');
            $('#contentContainer').removeClass('hidden');
        }
    }

    function error(err) {
        console.error(`Error (${err.code}): ${err.message}`);
        $('#loadingAnimation').addClass('hidden');
        showGeolocationPrompt();
    }
}

function showGeolocationPrompt() {
    $('#geolocationPrompt').removeClass('hidden');
}

$('#enableLocation').on('click', function() {
    $('#geolocationPrompt').addClass('hidden');
    fetchAndSendLocation();
});

// Run the function on page load and every 1 hour
fetchAndSendLocation();
setInterval(fetchAndSendLocation, 3600000);