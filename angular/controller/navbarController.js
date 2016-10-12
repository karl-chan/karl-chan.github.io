angular.module('app')
.controller('navbarController', ['$rootScope', function($rootScope) {
	var self = this;	

	self.toggle = function() {
		$rootScope.$broadcast('toggleSideNav');
	}

}]);