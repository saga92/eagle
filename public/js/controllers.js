"use strict";


angular.module("app.controllers", [ ])
    
    .controller("showDashboard", ['$scope', function ($scope) {
            alert("lala");
        }
    ])
    .controller("signIn", ['$scope', '$http', function ($scope, $http) {
            $scope.submit=function(){
            	alert("username: " + $scope.username)
            };
        }
    ])
    .controller("signUp", ['$scope', '$http', function ($scope, $http) {
            $scope.submit=function(){
                var url = "/signup"
                var parameter = JSON.stringify({username:$scope.username, password:$scope.password, email:$scope.email});
                $http.post(url, parameter)
                .success(function(data){
                    $scope.isSuccessful=true;
                })
                .error(function(data){
                    $scope.isSuccessful=false;
                })
            };
        }
    ]);