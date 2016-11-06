angular.module('cloud.resources', [])
    .factory('Overview', ['$resource', function ($resource) {        
        return $resource("/api/yunmall/overview/:id/:action/", {"id": "@id"},
            {
                getSummary: {isArray: false, params: {action: "summary"}}
            }
        );
    }])
    .factory('Fish', ['$resource', function ($resource) {        
        return $resource("/api/yunmall/fish/:id/:action/", {"id": "@id"},
            {
                query: {isArray: false}
            }
        );
    }])
    .factory('MobileBlack', ['$resource', function ($resource) {        
        return $resource("/api/yunmall/mobile-black/:id/:action/", {"id": "@id"},
            {
                query: {isArray: false}
            }
        );
    }])
;
