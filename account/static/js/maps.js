/* Set the width of the side navigation to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "262px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function openEmergency() {
   document.getElementById("emergency").style.marginBottom = "110px";
}

function closeEmergency() {
    document.getElementById("emergency").style.marginBottom = "0";
}

function openHospital() {
   document.getElementById("hospital").style.marginBottom = "110px";
}

function closeHospital() {
    document.getElementById("hospital").style.marginBottom = "0";
}

function openRoute() {
    document.getElementById("route").style.marginBottom = "200px";
    document.getElementById("mySidenav").style.width = "400px";
}

function closeRoute() {
    document.getElementById("route").style.marginBottom = "0";
    document.getElementById("mySidenav").style.width = "262px";
}

function openInterCity() {
    document.getElementById("interCity").style.marginBottom = "200px";
    document.getElementById("mySidenav").style.width = "400px";
}

function closeInterCity() {
    document.getElementById("interCity").style.marginBottom = "0";
    document.getElementById("mySidenav").style.width = "262px";
}

function openUserService() {
    document.getElementById("userService").style.marginBottom = "220px";

}

function closeUserService() {
    document.getElementById("userService").style.marginBottom = "0";

}


function showGoogleMaps(pos) {

	var latLng = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
	
    var mapOptions = {
        zoom: 16, // initialize zoom level - the max value is 21
        streetViewControl: false, // hide the yellow Street View pegman
        scaleControl: true, // allow users to zoom the Google Map
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        center: latLng
    };

    map = new google.maps.Map(document.getElementById('googleMaps'),
        mapOptions);

    // Show the default red marker at the location
    marker = new google.maps.Marker({
        position: latLng,
        map: map,
        draggable: false,
        animation: google.maps.Animation.DROP
    });
}


navigator.geolocation.getCurrentPosition(showGoogleMaps);

google.maps.event.addDomListener(window, 'load', showGoogleMaps);
