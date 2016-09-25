angular.module('app')
.controller('tagController', ['busObserverService', function(busObserverService) {
	var self = this;	

	self.getRegPlates = busObserverService.getRegPlates;
	self.getRoutes = busObserverService.getRoutes;
	
}]);