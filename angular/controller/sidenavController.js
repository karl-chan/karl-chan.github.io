angular.module('app')
.controller('sidenavController', ['$rootScope', 'busObserverService', function($rootScope, busObserverService) {
	var self = this;	

	self.isOpen = false;
	self.searchMethods = ['Reg plate', 'Route'];
	self.queryForm = {};

	self.selectedMethod = null;
	self.setSelected = function(method) {
		self.selectedMethod = method;
	}

	self.observe = function(method, observable) {
		busObserverService.observe(method, observable);
	}

	self.toggle = function() {
		self.isOpen ? self.close() : self.open();
		self.hideDrawerTip();
	}

	self.open= function () {
		self.isOpen = true;
		$('#mySidenav').width('250px');
		$('#main').css('marginLeft', '250px');
		$('#main').css('width', '100%').css('width', '-=250px');
	}

	self.close = function() {
		self.isOpen = false;
		$('#mySidenav').width('0');
		$('#main').css('marginLeft', '0');
		$('#main').css('width', '100%');
	}

	self.hideDrawerTip = function() {
		$('#drawerTip').hide('slow');
	}
	
	self.clearForms = function() {
		$('#mySidenav input').each(function() {
			$(this).val('');
		});
	}

	$rootScope.$on('toggleSideNav', function(event, args) {
		self.toggle();
	});

}]);