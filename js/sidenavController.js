angular.module('app')
.controller('sidenavController', ['busObserverService', function(busObserverService) {
	var self = this;	

	self.searchMethods = ['Reg plate', 'Route'];
	self.queryForm = {};

	self.selectedMethod = null;
	self.setSelected = function(method) {
		self.selectedMethod = method;
	}

	self.observe = function(method, observable) {
		busObserverService.observe(method, observable);
	}
}]);