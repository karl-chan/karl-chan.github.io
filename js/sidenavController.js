angular.module('app')
.controller('sidenavController', function() {
	var self = this;	

	self.searchMethods = ['Reg plate', 'Route'];

	self.selectedMethod = null;
	self.setSelected = function(method) {
		self.selectedMethod = method;
	}
});