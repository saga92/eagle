"use strict";

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when("/",
        {
            controller: "showDashboard",
            templateUrl: "dashboard.html"
        })
        .when("/signin",
        {
            controller: "signIn",
            templateUrl: "signin.html"
        })
        .when("/signup",
        {
            controller: "signUp",
            templateUrl: "signup.html"
        })
        .otherwise({ redirectTo: "/" });
    }
]);