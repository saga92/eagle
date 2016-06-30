"use strict";

angular.module("app.directives", [])
	.directive("disa", function($compile){
		return {
			terminal:true,
		    priority:1001,
		    compile: function(el) {
		      el.attr('disabled', 'disabled');
		      var fn = $compile(el);
		      return function(scope){
		        fn(scope);
		      };
		    }
		};
	});