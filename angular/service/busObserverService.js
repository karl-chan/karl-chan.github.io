angular.module('app')
.factory('busObserverService', ['$http', '$interval', '$window', function($http, $interval, $window) {
	var self = this;	

	var loopSeconds = 10;
	var tflCredentials;
	var routes;

	var regPlates = [];
	var routes = [];

	var map = $window.map;
	var targetBuses = [];
	var markers = []; // map from vehicleId to marker


	init = function() {
		$http.get('data/tflCredentials.json')
		.success(function(data) {
			tflCredentials = angular.fromJson(data);
		});
	}

	addTo = function(list, element) {	
		removeFrom(list, element) // avoid duplicates
		list.push(element);
	};

	removeFrom = function(list, element) {
		var index = list.indexOf(element);
		if (index != -1) {
			list.splice(index, 1);
		}
	};

	/* Fetch bus data from TfL api at regular intervals */
	// $interval(function() {
	// 	updateBuses();
	// }, loopSeconds * 1000);

	updateBuses = function() {
		newTargetBuses = [];
		_appendBusesByRegPlate(newTargetBuses);
		newTargetBuses = Array.from(new Set(newTargetBuses)); // remove duplicates
		updateMap(newTargetBuses, targetBuses);
		targetBuses = newTargetBuses;
	};

	_appendBusesByRegPlate = function(container) {
		if (regPlates.length > 0) {
			var vehicleList = regPlates.join(',')
			$http.get('https://api.tfl.gov.uk/Vehicle/'+vehicleList
				+'/Arrivals?app_id='+tflCredentials.app_id
				+'&app_key=' + tflCredentials.app_key)
			.then(function successCallback(response) {
				container.concat(response.data);
			}, function errorCallback(response) {

			});
		}
	};

	updateMap = function(newBuses, oldBuses) {
		for (var bus in newBuses) {
			var vehicleId = bus['vehicleId']
			if (vehicleId in oldBuses) {
				// update existing marker if bus already on map
				// newLatLng = new google.maps.LatLng(bus.)
				busMarker = markers[vehicleId]
				busMarker.setPosition
			} else {
				// add new marker since bus not yet on map
			}

			// look for buses withdrawn - remove marker from map
		}
	};

	init();

	return {
		observe: function(type, observable) {
			switch (type) {
				case 'Reg plate':
				addTo(regPlates, observable);
				break;
				case 'Route':
				addTo(routes, observable);
				break;
			}
		},
		remove: function(type, observable) {
			switch (type) {
				case 'Reg plate':
				removeFrom(regPlates, observable);
				break;
				case 'Route':
				removeFrom(routes, observable);
				break;
			}
		},
		getRegPlates: function() {
			return regPlates;
		},
		getRoutes: function() {
			return routes;
		},
	};
}]);