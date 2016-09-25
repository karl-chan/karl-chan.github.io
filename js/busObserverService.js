angular.module('app')
.factory('busObserverService', function() {
	var self = this;	

	self.regPlates = [];
	self.routes = [];

	addTo = function(list, element) {	
		removeFrom(list, element) // avoid duplicates
		list.push(element);
	};

	removeFrom = function(list, element) {
		var index = list.indexOf(element);
		if (index != -1) {
			list.splice(index, 1);
		}
	}

	return {
	    observe: function(type, observable) {
			switch (type) {
				case 'Reg plate':
				addTo(self.regPlates, observable);
				break;
				case 'Route':
				addTo(self.routes, observable);
				break;
			}
		},
		remove: function(type, observable) {
			switch (type) {
				case 'Reg plate':
				removeFrom(self.regPlates, observable);
				break;
				case 'Route':
				removeFrom(self.routes, observable);
				break;
			}
		},
		getRegPlates: function() {
			return self.regPlates;
		},
		getRoutes: function() {
			return self.routes;
		},
	}
});