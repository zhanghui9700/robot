(function(angular, moment, sprintf) {
    'use strict';

    angular.module('cloud.services', ["ngLodash"])
        .constant('moment', moment)
        .constant('sprintf', sprintf)
        .factory('Toolkit', Toolkit)
        .factory('PriceTool', PriceTool)
        .factory('QuotaTool', QuotaTool)
        .factory('ToastrService', ToastrService)
        .factory("AuthInterceptor", AuthInterceptor)
        .factory('settings', metronicSettings)
        .factory('ValidationTool', ValidationTool)
        .factory("CommonHttpService", CommonHttpService)
        .factory('ResourceTool', ResourceTool)
        .factory('CheckboxGroup', CheckboxGroup)
        .factory('DatePicker', DatePicker)
        .factory('ngTableHelper', ngTableHelper)
        .factory('UserProfileService', UserProfileService)
        .factory('timeService', timeService)
        .factory('BootboxService', BootboxService)
        .factory('CreateEchartOption', CreateEchartOption)
        .factory('getClusterMonitor', getClusterMonitor)
        .factory('changeCapacityUnit', changeCapacityUnit)
        .filter("humanizeDiskSize", humanizeDiskSize)
        .filter("humanizeTime", humanizeTime);

    function getClusterMonitor($state) {
        return function(host) {
            $state.go('cluster_detail', {
                "host": host,
            }, { location: false } );
        }
    }

    function changeCapacityUnit() {
        
        var lineCapacityUnit = function(items, point) {
            if(items && items[0][point[0]]>1000 && (items[0][point[0]] / 1024) < 1000) {
                items.map(function(x){
                    for(var i in point) {
                        x[point[i]] = ( x[point[i]] / 1024 ).toFixed(2)
                    }
                    x['unit'] = 'GB'
                });
            }else if(items && (items[0][point[0]] / 1024) > 1000){
                items.map(function(x){
                    for(var i in point) {
                        x[point[i]] = ( x[point[i]] / Math.pow(1024, 2) ).toFixed(2)
                    }
                    x['unit'] = 'TB'
                });
            }
        };
        function unit(items, point, unitArray) {
            if(items && (items[0][point[0]] > 1024)) {
                items.map(function(x){
                    for(var i in point) {
                        x[point[i]] = ( x[point[i]] / 1024 ).toFixed(2)
                    }
                    x['unit'] = unitArray[0];
                });
            }else if(items && (items[0][point[0]] < 1)) {
                items.map(function(x){
                    for(var i in point) {
                        x[point[i]] = ( x[point[i]] * 1024 ).toFixed(2)
                    }
                    x['unit'] = unitArray[1];
                });
            }
        };
        var lineNetSpeedUnit = function(items, point) {
            unit(items, point, ['Mb/s', 'b/s']);
        };
        var lineBandwidthUnit = function(items, point) {
            unit(items, point.slice(0,2), ['GB/s', 'KB/s'])
        }
        var capacityUnit = function(total, used, free) {
            var capacity = null;
            if ((total / 1024) < 1000) {
                capacity = {
                    used: (used / 1024).toFixed(1),
                    free: (free / 1024).toFixed(1),
                    total: (total / 1024).toFixed(1),
                    unit: 'GB',
                }
            } else {
                capacity = {
                    used: (used / Math.pow(1024, 2)).toFixed(1),
                    free: (free / Math.pow(1024, 2)).toFixed(1),
                    total: (total / Math.pow(1024, 2)).toFixed(1),
                    unit: 'TB',
                }
            }
            return capacity;
        };
        return {
            capacityUnit: capacityUnit,
            lineCapacityUnit: lineCapacityUnit,
            lineNetSpeedUnit: lineNetSpeedUnit,
            lineBandwidthUnit: lineBandwidthUnit,
        };
    }

    function Toolkit(ValidationTool, ngTableHelper,
        CommonHttpService, ToastrService, BootboxService, lodash, timeService, ResourceTool) {

        return {
            validate: ValidationTool.init,
            pagination: ngTableHelper,
            http: CommonHttpService,
            toastr: ToastrService,
            time: timeService,
            copyData: copyData,
            isEmpty: isEmpty,
            sprintf: sprintf,
            bootbox: BootboxService,
            resource: ResourceTool,
            static: getStatic(),
            checkbox: CheckboxGroup()
        };

        function getStatic() {
            return {
                "cloudView": function(path) {
                    return "/static/cloud/views/" + path + "?t=" + Math.random();
                },
                "cloudCtl": function(path) {
                    return "/static/cloud/controllers/" + path + "?t=" + Math.random();
                },

                "adminView": function(path) {
                    return "/static/management/views/" + path + "?t=" + Math.random();
                },
                "adminCtl": function(path) {
                    return "/static/management/controllers/" + path + "?t=" + Math.random();
                }
            };
        }

        function copyData(data) {
            var result = {};
            for (var attr in data) {
                if (attr.startsWith('$') || typeof data[attr] == 'function') {
                    continue;
                }
                result[attr] = data[attr];
            }

            return result;
        }

        function isEmpty(value) {
            if (value == null || value == undefined) {
                return true;
            }

            if (typeof value == 'string') {
                return /^\s*$/.test(value);
            }

            if (angular.isArray(value)) {
                return value.length == 0;
            }

            return lodash.keys(value).length == 0;
        }
    }

    function QuotaTool(CommonHttpService) {
        var init = function(quota) {
            var quotaExceed = function(resource, current) {
                var current = current || 0;
                if (quota.usages[resource].quota <= 0) {
                    return false;
                } else {
                    return quota.usages[resource].used + current > quota.usages[resource].quota;
                }
            };

            var calculateResourcePercent = function(resource, current) {
                var current = current || 0;
                if (quota.usages[resource].quota <= 0) {
                    return 0;
                } else {
                    return (quota.usages[resource].used + current) / quota.usages[resource].quota * 100;

                }
            };

            var calculateResourcePercentStyle = function(resource, current) {
                var current = current || 0;
                return "" + calculateResourcePercent(resource, current) + "%";
            };

            var getQuotaUsage = function() {
                return CommonHttpService.get("/api/quotas/usage/");
            };

            return {
                "items": quota.items,
                "usages": quota.usages,
                "isExceed": quotaExceed,
                "usedRatio": calculateResourcePercent,
                "usedRatioStr": calculateResourcePercentStyle
            }
        };

        return {
            init: init
        }
    }

    function BootboxService($i18next, $ngBootbox) {
        var confirm = function(title, msg, confirmed, canceled) {
            $ngBootbox.confirm(title, msg).then(confirmed, canceled);
        };
        return {
            "confirm": confirm
        }
    }

    function PriceTool($interpolate, lodash) {

        var diffFormat = $interpolate("{[{ price }]} + (n - {[{ flavor_start -1 }]}) * {[{ diff_price }]}");

        var hourPriceFormat = function(rule) {
            return diffFormat({
                price: rule.hour_price,
                diff_price: rule.hour_diff_price,
                flavor_start: rule.resource_flavor_start
            });
        };

        var monthPriceFormat = function(rule) {
            return diffFormat({
                price: rule.month_price,
                diff_price: rule.month_diff_price,
                flavor_start: rule.resource_flavor_start
            });
        };

        var getPrice = function(prices, flavor, payType) {

            prices = lodash.filter(prices, function(price) {
                return flavor >= price.resource_flavor_start;
            });

            var price = null;
            if (prices.length > 0) {
                price = prices.pop();
            } else {
                price = {
                    hour_price: 0,
                    month_price: 0,
                    price_type: 'normal'
                }
            }

            if (payType == 'hour') {
                price.price = price.hour_price;
                price.diff_price = price.hour_diff_price;
            } else {
                price.price = price.month_price;
                price.diff_price = price.month_diff_price;
            }

            if (price.price_type != 'diff') {
                return price.price;
            } else {
                return price.price + (flavor - price.resource_flavor_start + 1) * price.diff_price;
            }
        };

        return {
            hourPriceFormat: hourPriceFormat,
            monthPriceFormat: monthPriceFormat,
            getPrice: getPrice
        };
    }

    function humanizeDiskSize() {
        return function(size) {
            var units = ['MB', 'GB', 'TB', 'PB'];

            for (var i = 0; i < units.length; i++) {
                if (size < 1000) {
                    return "" + size + units[i];
                } else {
                    size /= 1000;
                }
            }
        };
    }

    function ToastrService($i18next) {
        toastr.options = {
            "closeButton": true,
            "debug": false,
            "positionClass": "toast-top-right",
            "onclick": null,
            "showDuration": "1000",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        };

        return {
            success: function(message, title) {
                title = title || $i18next('toastr.success');
                toastr.success(message, title);
            },
            warning: function(message, title) {
                title = title || $i18next('toastr.warning');
                toastr.warning(message, title);
            },
            error: function(message, title) {
                title = title || $i18next('toastr.error');
                toastr.error(message, title);
            }
        };

    }

    function AuthInterceptor($q) {
        return {
            'responseError': function(rejection) {
                if (rejection.status == 403 || rejection.status == 401) {
                    window.location.href = "/login/";
                    return $q.reject(rejection);
                }
                return rejection;
            }
        }
    }

    function metronicSettings($rootScope) {
        Metronic.setAssetsPath("/static/assets/");
        var settings = {
            layout: {
                pageSidebarClosed: false, // sidebar menu state
                pageBodySolid: false, // solid body color state
                pageAutoScrollOnLoad: 1000 // auto scroll to top on page load
            },
            layoutImgPath: Metronic.getAssetsPath() + 'admin/layout/img/',
            layoutCssPath: Metronic.getAssetsPath() + 'admin/layout/css/'
        };
        $rootScope.settings = settings;

        return settings;
    }

    function ValidationTool() {

        var defaultConfig = {
            onkeyup: false,
            doNotHideMessage: true,
            errorElement: 'span',
            errorClass: 'help-block help-block-error',
            focusInvalid: false,
            errorPlacement: function(error, element) {
                //element.parent().append(error);
                var p = element.parent();
                if (p && p.hasClass("input-group")) {
                    p = p.parent();
                }
                p.append(error);
            },

            highlight: function(element) {
                $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
            },

            unhighlight: function(element) {
                $(element).closest('.form-group').removeClass('has-error').addClass('has-success');
            }
        };

        return {
            init: function(selector, config) {
                config = config || {};
                for (var attr in defaultConfig) {
                    if (config[attr] === undefined) {
                        config[attr] = defaultConfig[attr];
                    }
                }
                $(selector).validate(config);

                return $(selector);
            },
            addValidator: $.validator.addMethod
        }
    }

    function CommonHttpService($http, $q) {
        return {
            'get': function(api_url) {
                var defer = $q.defer();
                $http({
                    method: 'GET',
                    url: api_url
                }).success(function(data, status, headers, config) {
                    defer.resolve(data);
                }).error(function(data, status, headers, config) {
                    defer.reject(data);
                });
                return defer.promise;
            },
            'post': function(api_url, post_data) {
                var defer = $q.defer();
                $http({
                    method: 'POST',
                    url: api_url,
                    data: $.param(post_data)
                }).success(function(data, status, headers, config) {
                    defer.resolve(data);
                }).error(function(data, status, headers, config) {
                    defer.reject(data);
                });
                return defer.promise;
            }
        };
    }

    function ResourceTool() {
        return {
            'copy_only_data': function(data) {

                var result = {};

                for (var attr in data) {
                    if (attr.startsWith('$') || attr == 'toJSON') {
                        continue;
                    }
                    result[attr] = data[attr];
                }

                return result;
            }
        }
    }

    function CheckboxGroup() {

        var init = function(objects, flagName) {

            flagName = flagName || 'checked';

            var groupChecker = {
                objects: objects,
                toggleAll: function() {
                    var self = this;
                    angular.forEach(self.objects, function(obj) {
                        obj[flagName] = self[flagName];
                    });
                },
                noneChecked: function() {
                    var count = 0;

                    angular.forEach(this.objects, function(obj) {
                        if (obj[flagName]) {
                            count += 1;
                        }
                    });

                    return count == 0;
                },
                syncObjects: function(objects) {
                    this.objects = objects;
                },
                uncheck: function() {
                    this[flagName] = false;
                    this.toggleAll();
                },
                forEachChecked: function(func) {
                    angular.forEach(this.objects, function(obj) {
                        if (obj[flagName]) {
                            func(obj);
                        }
                    });
                },
                checkedObjects: function() {
                    var results = [];
                    this.forEachChecked(function(obj) {
                        results.push(obj);
                    });
                    return results;
                }
            };

            groupChecker[flagName] = false;

            return groupChecker;
        };

        return {
            init: init
        };

    }

    function DatePicker() {

        /* Init date pickers, more functions come later. */
        var initDatePickers = function(selector) {

            selector = selector || '.date-picker';
            if (jQuery().datepicker) {
                $(selector).datepicker({
                    rtl: Metronic.isRTL(),
                    orientation: "left",
                    format: 'yyyy-mm-dd',
                    autoclose: true
                });
            }
        };

        var initDateTimePickers = function(config) {

            config = config || {};

            var defaultConfig = {
                autoclose: true,
                isRTL: Metronic.isRTL(),
                pickerPosition: (Metronic.isRTL() ? "bottom-right" : "bottom-left"),
                format: "yyyy-mm-dd hh:ii",
                todayBtn: true,
                minuteStep: 10
            };

            angular.extend(defaultConfig, config);

            $(".form_datetime").datetimepicker(defaultConfig);
        };

        return {
            initDatePickers: initDatePickers,
            initDateTimePickers: initDateTimePickers
        }
    }

    function ngTableHelper() {

        return {
            countPages: countPages,
            paginate: paginate,
            receiveData: receiveData,
            extend: extendTable
        };

        function paginate(data, $defer, params) {

            if (!angular.isArray(data)) {
                return data;
            }

            countPages(params, data.length);

            var start = (params.page() - 1) * params.count(),
                end = params.page() * params.count(),
                partial = data.slice(start, end);

            $defer.resolve(partial);

            return partial;
        }

        function countPages(params, total) {

            params.total(total);

            var pageNum = Math.ceil(total / params.count());

            if (pageNum == 0) {
                pageNum = 1;
            }

            if (pageNum < params.page()) {
                params.page(pageNum);
            }
        }

        function receiveData(data, $defer, params) {

            if (angular.isArray(data)) {
                paginate(data, $defer, params);
            }

            if (angular.isObject(data)) {
                $defer.resolve(data.results);
                countPages(params, data.count);
            }
        }

        function extendTable(table, conditionFunc) {

            table.ext = {
                query: search,
                keypress: keypress,
                getParams: searchParams
            };

            function search() {
                table.page(1);
                table.reload();
            }

            function keypress($event) {
                if ($event.keyCode == 13) {
                    $event.preventDefault();
                    search();
                }
            }

            function searchParams(params) {
                var result = {
                    page: params.page(),
                    page_size: params.count()
                };

                var condition = conditionFunc;

                if (angular.isFunction(condition)) {
                    condition = condition();
                }

                angular.extend(result, condition);

                return result;
            }
        }
    }

    function UserProfileService($modal) {

        var openProfileModal = function() {
            $modal.open({
                templateUrl: '/static/scripts/views/profile.html',
                backdrop: "static",
                controller: ProfileController,
                size: 'md'
            });
        };

        var openPasswordModal = function() {
            $modal.open({
                templateUrl: '/static/scripts/views/change-password.html',
                controller: ChangePasswordController,
                backdrop: "static",
                size: 'md'
            });
        };

        return {
            openProfileModal: openProfileModal,
            openPasswordModal: openPasswordModal
        };
    }

    function ProfileController($scope, $modalInstance, $i18next, $window, $timeout,
        CommonHttpService, ValidationTool, ToastrService) {

        var form = null;

        $scope.user = angular.copy($scope.current_user);
        $scope.cancel = $modalInstance.dismiss;

        $modalInstance.rendered.then(function() {
            form = ValidationTool.init('#profileForm');
        });

        $scope.save = function() {

            if (!form.valid()) {
                return;
            }

            CommonHttpService.post('/api/users/change-profile/', $scope.user).then(function(result) {
                if (result.success) {
                    ToastrService.success(result.msg, $i18next("success"));
                    $scope.current_user.mobile = $scope.user.mobile;
                    $scope.current_user.email = $scope.user.email;
                    $modalInstance.close();
                } else {
                    ToastrService.error(result.msg, $i18next("op_failed"));
                }
            });
        }
    }

    function ChangePasswordController($scope, $modalInstance, $i18next, $window, $timeout, ngTableParams,
        CommonHttpService, ValidationTool, ToastrService) {

        var form = null;

        $scope.params = {
            old_password: '',
            new_password: '',
            confirm_password: ''
        };
        $scope.cancel = $modalInstance.dismiss;

        $modalInstance.rendered.then(function() {
            form = ValidationTool.init('#passwordForm');
        });

        $scope.changePassword = function() {

            if (!form.valid()) {
                return;
            }

            CommonHttpService.post('/api/users/change-password/', $scope.params).then(function(result) {
                if (result.success) {
                    ToastrService.success(result.msg, $i18next("success"));
                    $modalInstance.close();
                    $timeout(function() {
                        window.location.href = "/login/";
                    }, 5000);
                } else {
                    ToastrService.error(result.msg, $i18next("op_failed"));
                }
            });
        }
    }

    var SECOND = 1000,
        MINUTE = 60 * SECOND,
        HOUR = 60 * MINUTE,
        DAY = 24 * HOUR,
        WEEK = 7 * DAY,
        MONTH = 30 * WEEK,
        YEAR = 365 * DAY,
        UNITS = [{
            value: YEAR,
            label: 'y',
            label_cn: '年'
        }, {
            value: MONTH,
            label: 'M',
            label_cn: "月"
        }, {
            value: WEEK,
            label: 'w',
            label_cn: "周"
        }, {
            value: DAY,
            label: 'd',
            label_cn: "天"
        }, {
            value: HOUR,
            label: 'h',
            label_cn: "时"
        }, {
            value: MINUTE,
            label: 'm',
            label_cn: "分"
        }, {
            value: SECOND,
            label: 's',
            label_cn: "秒"
        }];

    function humanizeTime() {
        return function(time) {
            var unit = null,
                result = '';

            for (var i = 0; i < UNITS.length; i++) {
                unit = UNITS[i];

                if (time >= unit.value) {
                    result += Math.round(time / unit.value) + unit.label_cn
                    time = time % unit.value
                }
            }
            return result;
        };
    }

    function timeService() {

        return {
            computeInterval: computeInterval,
            humanize: humanize
        };

        function computeInterval(start, end, num) {

            start = moment(start).valueOf();
            end = moment(end).valueOf();

            var duration = Math.abs(end - start),
                interval = duration / num;

            var unit = null;
            for (var i = 0; i < UNITS.length; i++) {
                unit = UNITS[i];
                if (interval > unit.value) {
                    interval = Math.round(interval / unit.value);
                    break;
                }
            }

            if (interval > 10) {
                interval = Math.round(interval / 10.0) * 10;
            }
            return interval + unit.label;
        }

        function humanize(time) {
            var unit = null,
                result = '';

            for (var i = 0; i < UNITS.length; i++) {
                unit = UNITS[i];

                if (time >= unit.value) {
                    result += Math.round(time / unit.value) + unit.label_cn
                    time = time % unit.value
                }
            }
            return result;
        }
    }

    function CreateEchartOption(lodash) {

        function setMax(max) {
            var max = 2 * Math.ceil(max);
            if (max >= 10) {
                var len = max.toString().length;
                var ji = Math.pow(10, len - 1);
                max /= ji;
                max = Math.round(max);
                max = max * ji;
            }
            return max;
        }

        function optionBase(opt, items, tit, unit){
            return {
                title: {text: tit},
                legend: {data: opt.legend},
                xAxis: {data: lodash.map(items, 'time')}
            }
        }

        var lineCreateOptions = function(opt, items, tit, unit) {
            var newOpt = optionBase(opt, items, tit, unit);
            newOpt.yAxis = [{
                    name: unit,
                    type: 'value',
                    boundaryGap: [0, '100%'],
                },];
            newOpt.series = [];
            for (var i = 0; i < opt.series.length; i++) {
                var ser = {
                    name: opt.legend[i],
                    data: lodash.map(items, opt.series[i]),
                }
                newOpt.series.push(ser);
            }
            return newOpt;
        };

        var twolineCreateOptions = function(opt, items, tit, unit) {
            var newOpt = optionBase(opt, items, tit, unit);    
            newOpt.series = [];

            var maxArray = [];

            for (var i = 0; i < opt.series.length; i++) {
                var sdata = lodash.map(items, opt.series[i]);
                var mdata = sdata.filter(function(element) {
                    return element !== undefined;
                });
                maxArray.push(Math.max.apply(null, mdata));

                var ser = {
                    name: opt.legend[i],
                    data: sdata,
                }
                if(opt.legend[i]=='iops' || 
                    opt.legend[i]=='read.ops' ||
                    opt.legend[i]=='write.ops' ){
                    ser['yAxisIndex'] = 1;
                }else{
                    ser['yAxisIndex'] = 0;
                }
                newOpt.series.push(ser);
            }

            var max1 = setMax(Math.max.apply(null, maxArray.slice(0, 2)));
            var max2 = setMax(Math.max.apply(null, maxArray.slice(2, maxArray.length)));

            newOpt.yAxis = [{
                name: unit,
                type: 'value',
                boundaryGap: [0, '100%'],
                min:0,
                max: max1,
                interval: max1 / 5,
            }, {
                name: 'IOPS',
                type: 'value',
                boundaryGap: [0, '100%'],
                min:0,
                max: max2,
                interval: max2 / 5,
            }];
            return newOpt;
        };

        return {
            'lineCreateOptions': lineCreateOptions,
            'twolineCreateOptions': twolineCreateOptions,
        };
    }

}(angular, moment, sprintf));