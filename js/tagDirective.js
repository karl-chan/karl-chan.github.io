angular.module('app')
.directive('tag', ['busObserverService', function(busObserverService) {
	return {
		restrict: 'E',
		scope: {
			type: '@',
			label: '@',
		},
		template: '<span>{{label}}<a href="javascript:void(0)" class="closebtn" ng-click="removeTag()">&times;</a></span>',
		link: function($scope, element, attrs) {
			$scope.removeTag = function() {
				busObserverService.remove(attrs.type, attrs.label);
			}
		},
	};
}]);