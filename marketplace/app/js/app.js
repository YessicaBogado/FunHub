'use strict';

angular.module('funhub', [
        'ngRoute',
        'funhub.filters',
        'funhub.controllers',
        'funhub.services',
        'funhub.directives',
        'ui.bootstrap',
        'wu.masonry',
        'ngCookies'
    ]).
    config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/registry', {templateUrl: 'partials/registry.html', controller: 'RegistryCtrl'});
        $routeProvider.when('/subscriptions', {templateUrl: 'partials/subscriptions.html', controller: 'StreamCtrl'});
        $routeProvider.when('/favorites', {templateUrl: 'partials/favorites.html', controller: 'FavoritesCtrl'});
        $routeProvider.when('/settings', {templateUrl: 'partials/settings.html', controller: 'SettingsCtrl'});
        $routeProvider.when('/about', {templateUrl: 'partials/about.html'});
        $routeProvider.when('/profile', {templateUrl: 'partials/profile.html'});
        $routeProvider.when('/uploadFunction', {templateUrl: 'partials/uploadFunction.html'});
        $routeProvider.otherwise({redirectTo: '/registry'});
    }]);
