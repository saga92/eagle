"use strict";


angular.module("app.controllers", [ ])
    
    .controller("showDashboard", ['$scope', function ($scope) {
            alert("lala");
        }
    ])
    .controller("signIn", ['$scope', function ($scope, $http) {
            $scope.submit=function(){
            	alert("username: " + $scope.username)
            };
        }
    ]);