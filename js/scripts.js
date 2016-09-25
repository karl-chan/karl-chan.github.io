function toggleNav() {
	var width = parseInt(document.getElementById('mySidenav').style.width, 0);
	if (width > 0) {
		closeNav();
	} else {
		openNav();
	}
	hideDrawerTip();
}

function openNav() {
	$('#mySidenav').width('250px');
	$('#main').css('marginLeft', '250px');
	$('#main').css('width', '100%').css('width', '-=250px');
}

function closeNav() {
	$('#mySidenav').width('0');
	$('#main').css('marginLeft', '0');
	$('#main').css('width', '100%');
}

function hideDrawerTip() {
	$('#drawerTip').hide('slow');
}

function resetForm() {	
	$('.queryInput').val('');
}

/* Google map */
var map;
function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
		center: {lat: 51.5074, lng: -0.1278}, // london
		zoom: 14,
	});


	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function (position) {
			initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
			map.setCenter(initialLocation);
		});
	}
};

$(document).ready(function() {
	$('body').fadeIn('slow');

})
