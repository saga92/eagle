"use strict";

angular.module("app.services", [])
	.factory('Session', ['$http', function($http){
		return {
			get: function(key, callback){
				$http.get("/_session?key=" + key).success(function(res){
					callback(res)
				})
			}
		}
	}])
	.filter('filterStat', function() {
		function decorateFilter(input) {
			var stat;
			if(input == 1){
				stat = "running"; 
			}else if(input == 2){
				stat = "stopped"
			}
    		return stat;
  		}
  		return decorateFilter;
	})
	.filter('filterLabelStat', function() {
		function decorateFilter(input) {
			var labelClass;
			if(input == 1){
				labelClass = "success"; 
			}else if(input == 2){
				labelClass = "default"
			}
    		return labelClass;
  		}
  		return decorateFilter;
	});