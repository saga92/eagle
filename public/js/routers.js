"use strict";

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when("/",
        {
            controller: "showDashboard",
            templateUrl: function(){
                return "public/partials/dashboard.html?" + new Date()
            }
        })
        .when("/signin",
        {
            controller: "signIn",
            templateUrl: function(){
                return "public/partials/signin.html?" + new Date()
            }
        })
        .when("/signup",
        {
            controller: "signUp",
            templateUrl: function(){
                return "public/partials/signup.html?" + new Date()
            }
        })
        .otherwise({ redirectTo: "/" });
    }
]);
