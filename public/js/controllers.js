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
                {id:2, name:"centos 7"},
                {id:3, name:"fedora 23"},
                {id:4, name:"debian 8"}
            ];

            $scope.containerName = "dev-container";
            Session.get("user_profile", function(res){
                var signInUsername = res.username;
                $http.get("/list_ins", {
                    params: {
                        signin_username: signInUsername
                    }
                }).success(function(data){

                    for(var i=0; i<data.instances.length; ++i){
                            //alert(data.instances[i].status);
                            if(data.instances[i].status == 1){
                                data.instances[i].instance_status = true;
                            }else if(data.instances[i].status == 2){
                                data.instances[i].instance_status = false;
                                //alert(data.instances[i].instance_status);
                            }
                        }
                    $scope.instances = data.instances;
                    console.log($scope.instances);
                });
            });

            $scope.closeAlert = function(){
                $('#popup').hide();
            }

             $scope.createIns=function(){
                Session.get("user_profile", function(res){
                    var signInUsername = res.username;
                    var url = "/create_ins";
                    var parameter = JSON.stringify({
                        image_id: $scope.selectedImage.id,
                        container_name: $scope.containerName,
                        user_name: signInUsername
                    });

                    $http.post(url, parameter).success(function(data){                        
                        $scope.popup = data.message;
                        if(data.code == "0x1"){
                            $scope.instances.push(data.instance);
                            data.instance.instance_status=true;
                            $scope.popupstatus = 'success';
                            $scope.popHead = "SUCCESS!";
                        }else if(data.code == "0x8"){
                            $scope.popupstatus = 'danger';
                            $scope.popHead = "Ops!! FAIL";
                        }else{
                            $scope.popupstatus = 'danger';
                            $scope.popHead = "Ops!! FAIL";
                            $scope.popup = "It seems something bad occur";
                        }

                        $("#popup").fadeTo(500, 1).slideDown(500, function(){
                            $(this).show(); 
                        });
                        
                        window.setTimeout(function() {
                            if($('#popup').is(':visible')){
                                $("#popup").fadeTo(500, 0).slideUp(500, function(){
                                    $(this).hide(); 
                                });
                            }
                        }, 3000);
                        
                        
                    }).error(function(data){
                        $scope.popup = data.message;
                        $scope.popupstatus = 'danger';
                        $scope.popHead = "Ops!! FAIL";

                        $("#popup").fadeTo(500, 1).slideDown(500, function(){
                            $(this).show(); 
                        });
                        
                        window.setTimeout(function() {
                            $("#popup").fadeTo(500, 0).slideUp(500, function(){
                                $(this).hide(); 
                            });
                        }, 3000);

                    });
                });
            };

            $scope.stopIns = function(containerSerial){
                Session.get("user_profile", function(res){
                    var signInUsername = res.username;
                    var url = "/stop_ins";
                    var parameter = JSON.stringify({
                        container_serial: containerSerial,
                        user_name: signInUsername
                    });

                    $http.post(url, parameter).success(function(data){
                        if(data.code == "0x1"){
                            for(var i=0; i<$scope.instances.length; ++i){
                                if($scope.instances[i].container_serial == data.container_serial){
                                    $scope.instances[i].status = 2;
                                    $scope.instances[i].instance_status = false;
                                    $scope.instances[i].host="-";
                                    $scope.instances[i].port="-";
                                    break;
                                }
                            }
                            $scope.popup = data.message;
                            $scope.popupstatus = 'success';
                            $scope.popHead = "SUCCESS!";
                        }else if(data.code == "0x3"){
                            $scope.popup = "api error";
                            $scope.popupstatus = 'danger';
                            $scope.popHead = "Ops!! FAIL";
                        }else{
                            $scope.popup = "unknown error";
                            $scope.popupstatus = 'danger';
                            $scope.popHead = "Ops!! FAIL";
                        }

                        $("#popup").fadeTo(500, 1).slideDown(500, function(){
                            $(this).show(); 
                        });
                        
                        window.setTimeout(function() {
                            $("#popup").fadeTo(500, 0).slideUp(500, function(){
                                $(this).hide(); 
                            });
                        }, 3000);

                    }).error(function(data){
                        $scope.popup = data.message;
                        $scope.popupstatus = 'danger';
                        $scope.popHead = "Ops!! FAIL";
                        $("#popup").fadeTo(500, 1).slideDown(500, function(){
                            $(this).show(); 
                        });
                        
                        window.setTimeout(function() {
                            $("#popup").fadeTo(500, 0).slideUp(500, function(){
                                $(this).hide(); 
                            });
                        }, 3000);
                    });
                });
            };

            $scope.restartIns = function(containerSerial){
                Session.get("user_profile", function(res){
                    var signInUsername = res.username;
                    var url = "/restart_ins";
                    var parameter = JSON.stringify({
                        container_serial: containerSerial,
                        user_name: signInUsername
                    });

                    $http.post(url, parameter).success(function(data){
                        if(data.code == "0x1"){
                            console.log(data);
                            for(var i=0; i<$scope.instances.length; ++i){
                                if($scope.instances[i].container_serial == data.container_serial){
                                    $scope.instances[i].status = 1;
                                    $scope.instances[i].instance_status = true;
                                    $scope.instances[i].host = data.host;
                                    $scope.instances[i].port = data.port;
                                    break;
                                }
                            }
                            $scope.popup = data.message;
                            $scope.popupstatus = 'success';
                            $scope.popHead = "SUCCESS!";
                        }else if(data.code == "0x3"){
                            $scope.popup = "api error";
                            $scope.popupstatus = 'danger';
                            $scope.popHead = "Ops!! FAIL";
                        }else{
                            $scope.popup = "unknown error";
                            $scope.popupstatus = 'danger';
                            $scope.popHead = "Ops!! FAIL";
                        }
                        $("#popup").fadeTo(500, 1).slideDown(500, function(){
                            $(this).show(); 
                        });
                        
                        window.setTimeout(function() {
                            $("#popup").fadeTo(500, 0).slideUp(500, function(){
                                $(this).hide(); 
                            });
                        }, 3000);
                    }).error(function(data){
                        $scope.popup = data.message;
                        $scope.popupstatus = 'danger';
                        $scope.popHead = "Ops!! FAIL";
                        $("#popup").fadeTo(500, 1).slideDown(500, function(){
                            $(this).show(); 
                        });
                        
                        window.setTimeout(function() {
                            $("#popup").fadeTo(500, 0).slideUp(500, function(){
                                $(this).hide(); 
                            });
                        }, 3000);
                    });
                });
            };


            $scope.rmIns = function(containerSerial){
                Session.get("user_profile", function(res){
                    var signInUsername = res.username;
                    var url = "/remove_ins";
                    var parameter = JSON.stringify({
                        container_serial: containerSerial,
                        user_name: signInUsername
                    });

                    $http.post(url, parameter).success(function(data){
                        if(data.code == "0x1"){
                            for(var i=0; i<$scope.instances.length; ++i){
                                if($scope.instances[i].container_serial == data.container_serial){
                                    $scope.instances.splice(i, 1);
                                    break;
                                }
                            }
                            $scope.popup = data.message;
                            $scope.popupstatus = 'success';
                            $scope.popHead = "SUCCESS!";
                        }else if(data.code == "0x3"){
                            $scope.popup = "api error";
                            $scope.popupstatus = 'danger';
                            $scope.popHead = "Ops!! FAIL";
                        }else{
                            $scope.popup = "unknown error";
                            $scope.popupstatus = 'danger';
                            $scope.popHead = "Ops!! FAIL";
                        }
                        $("#popup").fadeTo(500, 1).slideDown(500, function(){
                            $(this).show(); 
                        });
                        
                        window.setTimeout(function() {
                            $("#popup").fadeTo(500, 0).slideUp(500, function(){
                                $(this).hide(); 
                            });
                        }, 3000);

                    }).error(function(data){
                        $scope.popup = data.message;
                        $scope.popupstatus = 'danger';
                        $scope.popHead = "Ops!! FAIL";
                        $("#popup").fadeTo(500, 1).slideDown(500, function(){
                            $(this).show(); 
                        });
                        
                        window.setTimeout(function() {
                            $("#popup").fadeTo(500, 0).slideUp(500, function(){
                                $(this).hide(); 
                            });
                        }, 3000);
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
                    if(data.code == "0x1"){
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
                    if(data.code == "0x1"){
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
            Session.get("user_profile", function(res){
                $scope.signInUsername = res.username;
                $scope.signInPassword = res.password;
            });
        }
    ]);
