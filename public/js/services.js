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
				stat = "stopped";
			}else if(input == 3){
				stat = "failed";
			}
    		return stat;
  		}
  		return decorateFilter;
	})
	.filter('filterSerial', function() {
		function decorateFilter(input) {
			var serial = input;
			if(input == ''){
				serial = "-"; 
			}
    		return serial;
  		}
  		return decorateFilter;
	})
	.filter('filterHost', function() {
		function decorateFilter(input) {
			var host = input;
			if(input == ''){
				host = "-"; 
			}
    		return host;
  		}
  		return decorateFilter;
	})
	.filter('filterPort', function() {
		function decorateFilter(input) {
			var port = input;
			if(input == 0){
				port = "-"; 
			}
    		return port;
  		}
  		return decorateFilter;
	})
	.filter('filterDisabled', function() {
		function decorateFilter(input) {
			var stat = "";
			if(input == 3){
				stat = "disabled"; 
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
				labelClass = "default";
			}else if(input == 3){
				labelClass = "danger";
			}
    		return labelClass;
  		}
  		return decorateFilter;
	});