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
	}]);