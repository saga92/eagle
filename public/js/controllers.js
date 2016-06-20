"use strict";


angular.module("app.controllers", [ ])
    
    .controller("showDashboard", ['$scope', 'Session', '$http', '$window',
        function ($scope, Session, $http, $window) {
            Session.get('is_login', function(res){
                console.log(res);
                if(res != 'True'){
                    $window.location.href = '#/signin';
                }
            })
            $scope.images=[
                {id:1, name:"ubuntu 14.04"},
                {id:2, name:"centos 7"}
            ];
            $scope.containerName = "dev-container";
            Session.get("signin_user_name", function(res){
                var signInUsername = res;
                $http.get("/list_ins", {
                    params: {
                        signin_username: signInUsername
                    }
                }).success(function(data){
                    for(var i=0; i<data.instances.length; ++i){
                        data.instances[i].container_serial = data.instances[i].container_serial.substring(0,10);
                    }
                    data.statusStr = "stop";
                    console.log(data.statusStr);
                    $scope.instances = data.instances;
                    for(var i=0; i<$scope.instances.length; ++i){
                            if($scope.instances[i].status==2){
                                $scope.instances[i].statusStr = "restart";
                            }else if($scope.instances[i].status==1){
                                $scope.instances[i].statusStr = "stop";
                            }
                    }
                    console.log($scope.instances)
                });
            });
            
            $scope.createIns=function(){
                Session.get("signin_user_name", function(res){
                    var signInUsername = res;
                    var url = "/create_ins";
                    var parameter = JSON.stringify({
                        image_id: $scope.selectedImage.id,
                        container_name: $scope.containerName,
                        user_name: signInUsername
                    });

                    $http.post(url, parameter).success(function(data){
                        data.instance.container_serial = data.instance.container_serial.substring(0,10);
                        $scope.instances.push(data.instance);
                        $scope.popup = data.message;
                    }).error(function(data){
                        $scope.popup = data.message;
                    });
                });
            };

            $scope.stopIns = function(containerSerial){
                Session.get("signin_user_name", function(res){
                    var signInUsername = res;
                    var url = "/stop_ins";
                    var parameter = {
                        container_serial: containerSerial,
                        user_name: signInUsername
                    };
                    alert(parameter.container_serial);


                   $http.post(url, parameter).success(function(data){

                        for(var i=0; i<$scope.instances.length; ++i){
                            if($scope.instances[i].container_serial == data.container_serial){
                                if($scope.instances[i].status == 2){
                                    $scope.instances[i].status = 1;
                                    $scope.instances[i].statusStr ="stop";
                                    break;
                                }else if($scope.instances[i].status == 1){
                                    $scope.instances[i].status = 2;
                                    $scope.instances[i].statusStr ="restart";
                                    break;
                                }
                            }
                        }
                       $scope.popup = data.message;
                    }).error(function(data){
                        $scope.popup = data.message;
                    });
                });
            };

            $scope.rmIns = function(containerSerial){
                Session.get("signin_user_name", function(res){
                    var signInUsername = res;
                    var url = "/remove_ins";
                    var parameter = JSON.stringify({
                        container_serial: containerSerial,
                        user_name: signInUsername
                    });

                    $http.post(url, parameter).success(function(data){
                         for(var i=0; i<$scope.instances.length; ++i){
                            if($scope.instances[i].container_serial == data.container_serial){
                                $scope.instances.splice(i, i);
                                break;
                            }
                        }
                        $scope.popup = data.message;
                    }).error(function(data){
                        $scope.popup = data.message;
                    });
                });
            };

        }
    ])
    .controller("signIn", ['$scope', '$http', '$window', function ($scope, $http, $window) {
            $scope.submit=function(){
                var url = "/signin"
                var parameter = JSON.stringify({
                    username: $scope.username,
                    password: $scope.password
                });
            	$http.post(url, parameter).success(function(data){
                    if(data.code == 'ok'){
                        $window.location.href = '#/';
                    }else{
                        $scope.popup = data.message;
                    }
                }).error(function(data){
                    $scope.popup = data.message;
                });
            };
        }
    ])
    .controller("signUp", ['$scope', '$http', '$window', function ($scope, $http, $window) {
            $scope.submit=function(){
                var url = "/signup"
                var parameter = JSON.stringify({username:$scope.username, password:$scope.password, email:$scope.email});
                $http.post(url, parameter).success(function(data){
                    if(data.code == 'ok'){
                        $window.location.href = '#/';
                    }else{
                        $scope.popup=data.message;
                    }
                }).error(function(data){
                    $scope.popup=data.message;
                })
            };
        }
    ])
    .controller("getUsername", ['$scope', 'Session', '$http', '$window',
        function ($scope, Session, $http, $window) {
            Session.get("signin_user_name", function(res){
                $scope.signInUsername = res;
            });
        }
    ]);