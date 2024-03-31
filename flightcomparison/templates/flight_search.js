function searchFlights() {
    var departureLocation = document.getElementById("departure-location").value;
    var arrivalLocation = document.getElementById("arrival-location").value;
    var departureTime = document.getElementById("departure-time").value;
    var price = document.getElementById("price").value;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "{% url 'flight_search_data' %}?departure_location=" + departureLocation + "&arrival_location=" + arrivalLocation + "&departure_time=" + departureTime + "&price=" + price, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                document.getElementById("search-results").innerHTML = response;
            } else {
                console.error("Error: " + xhr.status);
            }
        }
    };
    xhr.send();
}
