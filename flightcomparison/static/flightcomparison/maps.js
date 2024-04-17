function map() {
    //data passed from the template
    var flight1 = null, flight2 = null;
    document.addEventListener('DOMContentLoaded', function() {
        var myElement = document.getElementById('map');
        flight1 = JSON.parse(myElement.getAttribute('data-flight1'));
        flight2 = JSON.parse(myElement.getAttribute('data-flight2'));  

        //intialzing map into the html div tag with id map

        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 5,
            center: { lat: 39.84937875926634, lng: -100.11546319759957 },
            mapTypeId: "terrain",
        });
    
        // coordinates and details
        const flightPlan1Coordinates = [
            { lat: parseFloat(flight1.departure_location_latitude), lng: parseFloat(flight1.departure_location_longitude), name: flight1.departure_location, dep_time: flight1.departure_time },
            { lat: parseFloat(flight1.layover_location_latitude), lng: parseFloat(flight1.layover_location_longitude), name: flight1.layover_location },
            { lat: parseFloat(flight1.arrival_location_latitude), lng: parseFloat(flight1.arrival_location_longitude), name: flight1.arrival_location, arr_time: flight1.arrival_time },
        ];


        console.log(flightPlan1Coordinates,"1")
        
    
        const flightPlan2Coordinates = [
            { lat: parseFloat(flight2.departure_location_latitude), lng: parseFloat(flight2.departure_location_longitude), name: flight2.departure_location },
            { lat: parseFloat(flight2.layover_location_latitude), lng: parseFloat(flight2.layover_location_longitude), name: flight2.layover_location },
            { lat: parseFloat(flight2.arrival_location_latitude), lng: parseFloat(flight2.arrival_location_longitude), name: flight2.arrival_location },
        ];

        console.log(flightPlan2Coordinates,"2")
    
    
        //creates path
    
        const flightPath1 = new google.maps.Polyline({
            path: flightPlan1Coordinates,
            geodesic: true,
            strokeColor: "#0000FF",
            strokeOpacity: 1.0,
            strokeWeight: 3,
        });
    
        
        const flightPath2 = new google.maps.Polyline({
            path: flightPlan2Coordinates,
            geodesic: true,
            strokeColor: "#EF7153",
            strokeOpacity: 1.0,
            strokeWeight: 3,
        });
    
        //creates markers
    
        flightPlan1Coordinates.forEach((coord, index) => {
            new google.maps.Marker({
                position: {lat: coord.lat, lng: coord.lng},
                map: map,
                title: coord.name,
                label: (index + 1).toString(),
            });
        });
    
        flightPlan2Coordinates.forEach((coord, index) => {
            new google.maps.Marker({
                position: {lat: coord.lat, lng: coord.lng},
                map: map,
                title: coord.name,
                label: (index + 1).toString(),
            });
        });
    
      
        flightPath1.setMap(map);
        flightPath2.setMap(map);
    
        // To display information of flight path
    
        //Flight 1
    
        //information overlay
        // const infoOverlay1 = new google.maps.OverlayView();
        // infoOverlay1.draw = function() {
        //     const projection = this.getProjection();
        //     const centerPixel = projection.fromLatLngToDivPixel(flightPlan1Coordinates[1]);
    
        //     const infoElement = document.createElement('div');
        //     infoElement.className = 'info-box';
        //     infoElement.style.position = 'absolute';
        //     infoElement.style.left = centerPixel.x  + 'px';
        //     infoElement.style.top = centerPixel.y + 'px';
        //     infoElement.innerHTML = `<div><b>${'Dep: ',new Date(flight1.departure_time),'Arr: ',flight1.arrival_time,'Price: $',flight1.price}<b></div>`;
        //     infoElement.style.zIndex = '100';
        //     infoElement.style.fontSize = 'large';
        //     infoElement.style.color = '#ff3333';
    
    
        //     this.getPanes().overlayLayer.appendChild(infoElement);
        // };
        // infoOverlay1.setMap(map);
    
        // // Flight 2
    
        // //overlay information
        // const infoOverlay2 = new google.maps.OverlayView();
        // infoOverlay2.draw = function() {
        //     const projection = this.getProjection();
        //     const centerPixel = projection.fromLatLngToDivPixel(flightPlan2Coordinates[1]);
    
        //     const infoElement = document.createElement('div');
        //     infoElement.className = 'info-box';
        //     infoElement.style.position = 'absolute';
        //     infoElement.style.left = centerPixel.x + 'px';
        //     infoElement.style.top = centerPixel.y + 'px';
        //     infoElement.innerHTML = `<div><b>${'Dep: ',flight2.departure_time,'Arr: ',flight2.arrival_time,'Price: $',flight2.price}<b></div>`;
        //     infoElement.style.zIndex = '100';
        //     infoElement.style.fontSize = 'large';
        //     infoElement.style.color = '#ff3333';
    
        //     this.getPanes().overlayLayer.appendChild(infoElement);
        // };
        // infoOverlay2.setMap(map);
    });
    

}

map();
  
