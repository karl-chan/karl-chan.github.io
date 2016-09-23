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


$(document).ready(function() {
	$('body').fadeIn('slow');
})
