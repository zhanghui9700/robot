/**
 * Created by zhanghui
 * Author: zhanghui9700@gmail.com
 * Date: 2015-05-04
 * Description: Main Cloud App
 */

'use strict';

/* Cloud App */
var CloudApp = angular.module("CloudApp", [
    "ui.router",
    "ui.bootstrap",
    "oc.lazyLoad",
    "ngSanitize",
    "ngTable",
    "ngResource",
    "ngCookies",
    "ngBootbox",
    "jm.i18next",
    "ngLodash",
    "cloud.services",
    "cloud.resources",
    "cloud.directives"
]);

CloudApp.config(function ($i18nextProvider) {
    $i18nextProvider.options = {
        lng: 'cn',
        fallbackLng: 'en',
        useCookie: false,
        useLocalStorage: false,
        resGetPath: '/api/i18n/__lng__.json'
    };
});

CloudApp.config(['$resourceProvider', function ($resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

CloudApp.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol("{[{");
    $interpolateProvider.endSymbol("}]}");
}]);

CloudApp.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Request-Width'];
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    $httpProvider.interceptors.push('AuthInterceptor');
}]);

CloudApp.config(['$ocLazyLoadProvider', function ($ocLazyLoadProvider) {
    $ocLazyLoadProvider.config({});
}]);

/* Setup global settings */
CloudApp.factory('settings', ['$rootScope', function ($rootScope) {
    // supported languages
    var settings = {
        layout: {
            pageSidebarClosed: false, // sidebar menu state
            pageBodySolid: false, // solid body color state
            pageAutoScrollOnLoad: 1000 // auto scroll to top on page load
        },
        //layoutImgPath: Metronic.getAssetsPath() + 'admin/layout/img/',
        //layoutCssPath: Metronic.getAssetsPath() + 'admin/layout/css/'
    };

    $rootScope.settings = settings;

    return settings;
}]);

/* Setup App Main Controller */
CloudApp.controller('AppController', ['$scope', '$rootScope', function ($scope, $rootScope) {
    $scope.$on('$viewContentLoaded', function () {
        Metronic.initComponents(); // init core components
    });
}]);

CloudApp.controller('HeaderController',
    ['$rootScope', '$scope', '$http', '$interval', 'UserProfileService',
        function ($rootScope, $scope, $http, $interval, Feed, UserProfileService) {
            $scope.$on('$includeContentLoaded', function () {
                Layout.initHeader(); // init header
            });
        }
    ]
);

/* Setup Layout Part - Sidebar */
CloudApp.controller('SidebarController', ['$scope', function ($scope) {
    $scope.$on('$includeContentLoaded', function () {
        Layout.initSidebar(); // init sidebar
    });
}]);

/* Setup Layout Part - Footer */
CloudApp.controller('FooterController', ['$scope', function ($scope) {
    $scope.$on('$includeContentLoaded', function () {
        Layout.initFooter(); // init footer
    });
}]);


CloudApp.provider("staticHelper", function () {
    this.cloudView = function (path) {
        return "/static/cloud/views/" + path + "?t=" + Math.random();
    };
    this.cloudCtl = function (path) {
        return "/static/cloud/controllers/" + path + "?t=" + Math.random();
    };
    this.adminView = function (path) {
        return "/static/management/views/" + path + "?t=" + Math.random();
    };
    this.adminCtl = function (path) {
        return "/static/management/controllers/" + path + "?t=" + Math.random();
    };

    this.$get = function () {
        return {
            'cloudView': this.cloudView,
            'cloudCtl': this.cloudCtl,
            'adminView': this.adminView,
            'adminCtl': this.adminCtl
        };
    };
});


/* Setup Rounting For All Pages */
CloudApp.config(['$stateProvider', '$urlRouterProvider', 'current_user', 'site_config', "staticHelperProvider",
    function ($stateProvider, $urlRouterProvider, current_user, site_config, staticHelperProvider) {

        $urlRouterProvider.otherwise("/overview/");
        $stateProvider
        // Overview
            .state('overview', {
                url: "/overview/",
                templateUrl: staticHelperProvider.cloudView("overview/overview.html"),
                data: {pageTitle: 'sidebar.overview'},
                controller: "OverviewController",
                resolve: {
                    deps: ['$ocLazyLoad', function ($ocLazyLoad) {
                        return $ocLazyLoad.load({
                            name: 'CloudApp',
                            insertBefore: '#ng_load_plugins_before',
                            files: [
                            ]
                        }).then(function () {
                            return $ocLazyLoad.load({
                                name: 'CloudApp',
                                insertBefore: '#ng_load_plugins_before',
                                files: [
                                    staticHelperProvider.cloudCtl("overview/overview_ctl.js"),
                                ]
                            });
                        });
                    }]
                }
            })        
        ;
    }]);

/* Init global settings and run the app */
CloudApp.run(["$rootScope", "settings", "$state", "$http", "$cookies",
                "$interval", "current_user", "site_config",
    function ($rootScope, settings, $state, $http, $cookies,
              $interval, current_user, site_config) {

        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
        
        $rootScope.$state = $state;
        $rootScope.timer_list = [];
        $rootScope.current_user = current_user;
        $rootScope.site_config = site_config;
        var callbacks = [];

        $rootScope.executeWhenLeave = function (callback) {
            callbacks.push(callback);
        };

        $rootScope.setInterval = function (func, interval) {
            var timer = $interval(func, interval);
            $rootScope.executeWhenLeave(function () {
                $interval.cancel(timer);
            });
        };

        $rootScope.$on("$stateChangeStart", function (e, toState, toParams, fromState, fromParams) {
            while ($rootScope.timer_list.length > 0) {
                var t = $rootScope.timer_list.pop();
                $interval.cancel(t);
            }

            angular.forEach(callbacks, function (callback) {
                callback();
            });

            callbacks = [];
        });
        
        $rootScope.$on("$routeChangeSuccess", function (e, toState, toParams, fromState, fromParams) {
            console.log(toState);
        });


        $rootScope.seed = Math.random();
    }]);
