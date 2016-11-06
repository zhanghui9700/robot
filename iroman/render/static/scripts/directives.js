angular.module('cloud.directives', [])

    .directive('title', ['$rootScope', '$timeout', '$window', 'site_config', "$i18next",
        function ($rootScope, $timeout, $window, site_config, $i18next) {
            return {
                restrict: 'E',
                link: function () {
                    var listener = function (event, toState) {
                        $timeout(function () {
                            var title = site_config.BRAND;

                            if (toState.data && toState.data.pageTitle) {
                                title += " | ";
                                title += $i18next(toState.data.pageTitle);
                            }

                            $window.document.title = title;
                        });
                    };
                    $rootScope.$on('$stateChangeSuccess', listener);
                }
            };
        }
    ])

    .directive('ngSpinnerBar', ['$rootScope',
        function ($rootScope) {
            return {
                link: function (scope, element, attrs) {
                    // by defult hide the spinner bar
                    element.addClass('hide'); // hide spinner bar by default

                    // display the spinner bar whenever the route changes(the content part started loading)
                    $rootScope.$on('$stateChangeStart', function () {
                        element.removeClass('hide'); // show spinner bar
                    });

                    // hide the spinner bar on rounte change success(after the content loaded)
                    $rootScope.$on('$stateChangeSuccess', function () {
                        element.addClass('hide'); // hide spinner bar
                        $('body').removeClass('page-on-load'); // remove page loading indicator
                        Layout.setSidebarMenuActiveLink('match'); // activate selected link in the sidebar menu

                        // auto scorll to page top
                        setTimeout(function () {
                            Metronic.scrollTop(); // scroll to the top on content load
                        }, $rootScope.settings.layout.pageAutoScrollOnLoad);
                    });

                    // handle errors
                    $rootScope.$on('$stateNotFound', function () {
                        element.addClass('hide'); // hide spinner bar
                    });

                    // handle errors
                    $rootScope.$on('$stateChangeError', function () {
                        element.addClass('hide'); // hide spinner bar
                    });
                }
            };
        }
    ])

    // Handle global LINK click
    .directive('a', function () {
        return {
            restrict: 'E',
            link: function (scope, elem, attrs) {
                if (attrs.ngClick || attrs.href === '' || attrs.href === '#') {
                    elem.on('click', function (e) {
                        e.preventDefault(); // prevent link click for above criteria
                    });
                }
            }
        };
    })

    // Handle Dropdown Hover Plugin Integration
    .directive('dropdownMenuHover', function () {
        return {
            link: function (scope, elem) {
                elem.dropdownHover();
            }
        };
    })

    .directive('napAfterClick', function ($timeout) {
        return {
            restrict: 'A',
            link: function (scope, elem, attrs) {

                var duration = parseInt(attrs.napAfterClick);

                if (isNaN(duration)) {
                    duration = 2;
                }

                duration *= 1000;

                elem.on('click', function () {
                    elem.addClass('disabled');
                    $timeout(function () {
                        elem.removeClass('disabled');
                    }, duration);
                });
            }
        };
    })

    .directive('eonDatePicker', function ($timeout, DatePicker) {
        return {
            link: function (scope, element, attrs) {
                $timeout(function () {
                    DatePicker.initDatePickers(element);
                });
            }
        };
    })

    .directive('eonHelp', function () {
        return {
            restrict: 'E',
            replace: true,
            template: "<a><i class=\"fa fa-question-circle eon-help\"></i></a>"
        }
    })

    .directive('eonSubmitting', function () {
        var t = "<a class=\"btn\"><img src=\"/static/assets/global/img/throbber.gif\"/></a>";
        var link = function (scope, ele, attrs) {
            scope.$watch("submitting", function (value) {
                if (value) {
                    $(ele).show()
                }
                else {
                    $(ele).hide()
                }
            });
        };

        return {
            restrict: 'E',
            replace: true,
            scope: {
                "submitting": "=submitting"
            },
            template: t,
            link: link
        }
    })


    .directive('lineChart', function () {
        return {
            restrict: 'A',
            scope: {
                options: "=",
            },
            link: function ($scope, element, attrs) {
                Metronic.unblockUI('#'+element.context.parentNode.parentNode.id);
                var options = $scope.options;
                var xAxis = angular.extend(xAxisTemplate(), options.xAxis);
                var yAxis = [{
                    type: 'value',
                    boundaryGap: [0, '100%']
                },];

                var series = genSeries(options.series);

                var optionTemplate = {
                    title: options.title,
                    tooltip: {
                        trigger: 'axis',
                        position: function (pt) {
                            return [pt[0], '10%'];
                        }
                    },
                    xAxis: xAxis,
                    yAxis: yAxis,
                    // toolbox: {
                    //     feature: {
                    //         saveAsImage: {}
                    //     }
                    // },
                    grid: {
                        left: '2%',
                        bottom: '4%',
                        containLabel: true
                    },
                    legend: options.legend,
                    series: series
                };

                var myChart = echarts.init(element[0]);
                myChart.setOption(optionTemplate);

                $scope.$watch("options", function (newOptions, oldValue) {
                    if (newOptions) {
                        myChart.setOption(setOptionDatas(newOptions));
                    }
                    myChart.resize();
                });

                $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
                    myChart.resize();
                });

                function setOptionDatas(options) {
                    return {
                        xAxis: angular.extend(xAxisTemplate(), options.xAxis),
                        yAxis: options.yAxis,
                        series: genSeries(options.series),
                        legend: options.legend,
                        title: options.title
                    }
                }

                function genSeries(configs) {

                    var series = [];

                    configs.forEach(function (config) {
                        series.push(angular.extend(serieTemplate(), config));
                    });

                    return series;
                }

                function xAxisTemplate() {
                    return {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    };
                }

                function serieTemplate() {
                    return {
                        name: '',
                        type: 'line',
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        areaStyle: {normal: {}},
                        data: []
                    };
                }
            }
        }
    })

    .directive('twolineChart', function () {
        return {
            restrict: 'A',
            scope: {
                options: "=",
            },
            link: function ($scope, element, attrs) {
                Metronic.unblockUI('#'+element.context.parentNode.parentNode.id);
                var options = $scope.options;
                var xAxis = angular.extend(xAxisTemplate(), options.xAxis);
                var yAxis = [{
                        type: 'value',
                        boundaryGap: [0, '100%'],
                    },{
                        type: 'value',
                        name: 'iops',
                        boundaryGap: [0, '100%'],
                    }];

                var series = genSeries(options.series);

                var optionTemplate = {
                    title: options.title,
                    tooltip: {
                        trigger: 'axis',
                        position: function (pt) {
                            return [pt[0], '10%'];
                        }
                    },
                    xAxis: xAxis,
                    yAxis: yAxis,
                    // toolbox: {
                    //     feature: {
                    //         saveAsImage: {}
                    //     }
                    // },
                    grid: {
                        left: '2%',
                        bottom: '4%',
                        containLabel: true
                    },
                    legend: options.legend,
                    series: series
                };

                var myChart = echarts.init(element[0]);
                myChart.setOption(optionTemplate);

                $scope.$watch("options", function (newOptions, oldValue) {
                    if (newOptions) {
                        myChart.setOption(setOptionDatas(newOptions));
                    }
                    myChart.resize();
                });

                $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
                    myChart.resize();
                });

                function setOptionDatas(options) {
                    return {
                        xAxis: angular.extend(xAxisTemplate(), options.xAxis),
                        yAxis: options.yAxis,
                        series: genSeries(options.series),
                        legend: options.legend,
                        title: options.title
                    }
                }

                function genSeries(configs) {

                    var series = [];

                    configs.forEach(function (config) {
                        series.push(angular.extend(serieTemplate(), config));
                    });

                    return series;
                }

                function xAxisTemplate() {
                    return {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    };
                }

                function serieTemplate() {
                    return {
                        name: '',
                        type: 'line',
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        areaStyle: {normal: {}},
                        data: []
                    };
                }
            }
        }
    })


    .directive('dashChart', function ($i18next) {
        return {
            restrict: 'A',
            scope: {
                options: "=",
            },
            link: function ($scope, element, attrs) {
                options = $scope.options
                option = {
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a}{b}: {c}%"
                    },
                    series: [
                        {
                            type: 'gauge',
                            min: 0,
                            max: 100,
                            splitNumber: 5,
                            radius: '80%',
                            axisLine: {
                                lineStyle: {
                                    color: [[0.16, '#1BA39C'], [0.82, '#546570'], [1, '#C23531']],
                                    width: 5,
                                }
                            },
                            axisTick: {
                                length: 3,
                            },
                            splitLine: {
                                length: 8,
                            },
                            pointer: {
                                width:2
                            },
                            title: {
                                textStyle: {
                                    fontSize: 12,
                                }
                            },
                            detail: {
                                textStyle: {
                                    fontSize: 18,
                                },
                                offsetCenter: [0, '80%'],
                            },
                            data: [{value: options.data, name: ''}]
                        }
                    ]
                };
                var myChart = echarts.init(element[0]);
                myChart.setOption(option);

                $scope.$watch('options', function (newOptions, oldvalue) {
                    myChart.setOption({
                        series: [{data: [{value: newOptions.data, name: $i18next("usage")+'(%)'}]}],
                    });
                });
            }
        }
    })

    .directive('circleChart', function ($i18next) {
        return {
            restrict: 'A',
            scope: {
                options: "=",
            },
            link: function ($scope, element, attrs) {
                options = $scope.options
                var labelTop = {
                    normal: {
                        // color: '#C23531',
                        color: 'green',
                        label: {
                            show: true,
                            position: 'center',
                            formatter: '{d}%',
                            textStyle: {
                                baseline: 'top'
                            }
                        },
                    }
                };
                var labelBottom = {
                    normal: {
                        color: '#bbb',
                        label: {
                            show: false,
                            position: 'center'
                        },
                    },
                };
                option = {
                    series: [
                        {
                            type: 'pie',
                            radius: [25, 35],
                            data: [
                                {name: 'used', value: 0, itemStyle: labelTop},
                                {name: 'free', value: 100, itemStyle: labelBottom},
                            ]
                        },
                    ]
                };
                var myChart = echarts.init(element[0]);
                myChart.setOption(option);

                $scope.$watch('options', function (newOptions, oldvalue) {
                    myChart.setOption({
                        series: [{
                            data: [{value: newOptions[0], itemStyle: labelTop}, {value: newOptions[1]}],
                            itemStyle: labelBottom
                        }]
                    });
                });
            }
        }
    })

    .directive('pieChart', function () {
        return {
            restrict: 'A',
            scope: {
                options: "=",
            },
            link: function ($scope, element, attrs) {
                options = $scope.options
                option = {
                    tooltip: {
                        // trigger: 'item',
                        formatter: "{b}: {c} ({d}%)"
                    },
                    legend: {
                        orient: 'vertical',
                        x: 'left',
                        data: options.legend
                    },
                    series: [
                        {
                            type: 'pie',
                            selectedMode: 'single',
                            radius: [0, '30%'],
                            data: options.pgSeriesData,
                            labelLine: {
                                normal: {
                                    show:false
                                },
                            },
                            label: {
                                normal: {
                                    show:false
                                }
                            },
                        },
                        {
                            type: 'pie',
                            radius: ['50%', '65%'],
                            data: options.totalSeriesData,
                        }
                    ]
                };
                var myChart = echarts.init(element[0]);
                myChart.setOption(option);

                $scope.$watch('options', function (newOptions, oldvalue) {
                    myChart.setOption({
                        legend: {data: newOptions.legend},
                        series: [{data: newOptions.pgSeriesData}, {data: newOptions.totalSeriesData}]
                    });
                });
            }
        }
    })

    .directive('slimscroll', function () {
        'use strict';

        return {
            restrict: 'A',
            link: function ($scope, $elem, $attr) {
                if (Metronic) {
                    Metronic.initSlimScroll($elem);
                }
            }
        };
    });

;
