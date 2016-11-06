(function (angular) {

    'use strict';
    
    angular.module('CloudApp')
        .controller('OverviewController', OverviewController)
        ;

    function OverviewController($rootScope, $scope, $i18next, ngTableParams, sprintf, Toolkit,
             Overview, Fish, MobileBlack) {
        $scope.$on('$viewContentLoaded', function () {
            Metronic.initAjax();
        }); 

        getSummary();

       $scope.fish_table = new ngTableParams({
            page: 1,
            count: 10
        },{
            counts: [],
            getData: function ($defer, params) {
                var filter = params.filter(),
                    searchParams = {page: params.page(), page_size: params.count()};
                Fish.query(searchParams, function (data) {
                    $defer.resolve(data.results);
                    Toolkit.pagination.countPages(params, data.count);
                });
            }
        }); 

       $scope.mobile_black_table = new ngTableParams({
            page: 1,
            count: 10
        },{
            counts: [],
            getData: function ($defer, params) {
                var filter = params.filter(),
                    searchParams = {page: params.page(), page_size: params.count()};
                MobileBlack.query(searchParams, function (data) {
                    $defer.resolve(data.results);
                    Toolkit.pagination.countPages(params, data.count);
                });
            }
        }); 

        $rootScope.setInterval(function () {
            getSummary(); 
            $scope.fish_table.page(1);
            $scope.mobile_black_table.page(1);
        }, 60000);

        function getSummary(){
            Overview.getSummary().$promise.then(function(summary){
                $scope.summary = summary; 
            });
        }

        function getRecentFish(){

        }
    }
}(angular));
