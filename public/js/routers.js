"use strict";

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when("/",
        {
            controller: "showDashboard",
            templateUrl: "public/partials/dashboard.html"
        })
        .when("/signin",
        {
            controller: "signIn",
            templateUrl: "public/partials/signin.html"
        })
        .when("/signup",
        {
            controller: "signUp",
            templateUrl: "public/partials/signup.html"
        })
        .when("/signout",
        {
            controller: "signOut",
            templateUrl: "public/partials/signin.html"
        })
        .otherwise({ redirectTo: "/" });
    }
]);