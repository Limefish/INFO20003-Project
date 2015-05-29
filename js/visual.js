var dataset

// Make a copy of the default Highcharts theme
var HCDefaults = $.extend(true, {}, Highcharts.getOptions(), {});

function ResetOptions() {
//Resets the Highcharts theme back to default
    var defaultOptions = Highcharts.getOptions();
    for (var prop in defaultOptions) {
        if (typeof defaultOptions[prop] !== 'function') delete defaultOptions[prop];
    }
    Highcharts.setOptions(HCDefaults);
}

$(document).ready(function() {
//Makes an AJAX request, where it collects all the data needed for the charts
//in the form of a json file.
    $.ajax({
        type: "GET",
        url: 'visual.py',
        dataType: 'json',
        success: function(data) {
            dataset = data
        }
    });
});

$(document).ajaxStop(function () {
//Waits until the AJAX request is finished
    //Generation of Charts
    $('.genderRatio').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: 'Gender Ratio of Comic Book Characters Introduced Each Year'
        },
        xAxis: {
            categories: dataset.genderYear.maleYear,
            tickmarkPlacement: 'on',
            title: {
                enabled: false
            },
            tickInterval: 6
        },
        yAxis: {
            title: {
                text: 'Percentage'
            },
            max: 1.1,
            endOnTick: false,
            tickPositions: [0,0.2,0.4,0.6,0.8,1],
            labels: {
                formatter: function () {
                    return this.value * 100;
                }
            }
        },
        tooltip: {
            shared: true,
            formatter: function () {
                var s = this.x;

                s += '<br/>' + '<span style="color:' + this.points[0].series.color + '">●</span>'
                + this.points[0].series.name + ': <b>' + (this.points[0].y * 100).toFixed(2) + '%</b>';

                s += '<br/>' + '<span style="color:' + this.points[1].series.color + '">♦</span>'
                + this.points[1].series.name + ': <b>' + (this.points[1].y * 100).toFixed(2) + '%</b>';

                s += '<br/>' + '<span style="color:' + this.points[2].series.color + '">■</span>'
                + this.points[2].series.name + ': <b>' + (this.points[2].y * 100).toFixed(2) + '%</b>';

                s += '<br/>' + '<span style="color:' + this.points[3].series.color + '">▲</span>'
                + this.points[3].series.name + ': <b>' + (this.points[3].y * 100).toFixed(2) + '%</b>';

                return s;
            },
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    enabled: false,
                    lineWidth: 1,
                    lineColor: '#666666'
                }
            }
        },
        series: [{
            name: 'Males',
            data: dataset.genderYear.maleValue
        }, {
            name: 'Females',
            data: dataset.genderYear.femaleValue
        }, {
            type: 'spline',
            name: 'Cumulative Males',
            data: dataset.genderYear.cumulativeMale,
            marker: {
                enabled: false,
                lineWidth: 2,
                lineColor: Highcharts.getOptions().colors[2],
                fillColor: Highcharts.getOptions().colors[2]
            }
        }, {
            type: 'spline',
            name: 'Cumulative Females',
            data: dataset.genderYear.cumulativeFemale,
            marker: {
                enabled: false,
                lineWidth: 2,
                lineColor: Highcharts.getOptions().colors[3],
                fillColor: Highcharts.getOptions().colors[3]
            }
        }]       
    });

    Highcharts.setOptions(Highcharts.theme);
    $('.genderCount').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Gender Count'
        },
        subtitle: {
            text: 'Gender Count of Males and Females'
        },
        xAxis: {
            categories: ['Male', 'Female', 'Others'],
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Count',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'horizontal',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 200,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Count',
            data: [dataset.genderCount.totalMale, dataset.genderCount.totalFemale, dataset.genderCount.totalOthers]
        }]
    });

    $('.sexualOrientation').highcharts({
        title: {
            text: 'Sexual Minorities by their First Year of Appearance',
            x: -20
        },
        xAxis: {
            categories: dataset.orientationYear.homoYear,
            tickInterval: 6
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Count'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        credits: {
            enabled: false
        },
        tooltip: {
            shared: true
        },
        plotOptions: {
            line: {
                marker: {
                    enabled: false
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'Total',
            data: [{
                name: 'Heterosexual',
                y: dataset.orientationAlign.totalHetero,
                color: Highcharts.getOptions().colors[2]
            }, {
                name: 'Homosexual',
                y: dataset.orientationAlign.totalHomo,
                color: Highcharts.getOptions().colors[0]
            }, {
                name: 'Bisexual',
                y: dataset.orientationAlign.totalBi,
                color: Highcharts.getOptions().colors[1]
            }, {
                name: 'Others',
                y: dataset.orientationAlign.totalOthers,
                color: '#045a8d'
            }],
            center: [180, 140],
            size: 300,
            enableMouseTracking: true,
            showInLegend: true,
            dataLabels: {
                enabled: true,
                formatter: function () {
                    return this.percentage.toFixed(2) + '%'
                }
            }
        }, {
            name: 'Homosexual',
            data: dataset.orientationYear.homoValue
        }, {
            name: 'Bisexual',
            data: dataset.orientationYear.biValue
        }]
    });

    ResetOptions();
    $('.goodGays').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Percentage of Character Alignment by Sexual Orientation'
        },
        xAxis: {
            categories: ['Heterosexual', 'Homosexual', 'Bisexual']
        },
        yAxis: {
            min: 0,
            max: 110,
            endOnTick: false,
            tickPositions: [0,20,40,60,80,100],
            title: {
                text: 'Percentage'
            },
            stackLabels: {
                enabled: false
            }
        },
        credits: {
            enabled: false
        },
        legend: {
            align: 'right',
            x: -30,
            verticalAlign: 'top',
            y: 25,
            floating: true,
            borderColor: '#CCC',
            borderWidth: 1,
            shadow: false
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' +
                    this.series.name + ': ' + this.y + '%<br/>' +
                    'Total: ' + this.point.stackTotal + '%';
            }
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true,
                    style: {
                        fontSize: '1em'
                    }
                }
            }
        },
        series: [{
            name: 'Bad',
            color:'#f03b20',
            data: [dataset.orientationAlign.hetero['bad'], dataset.orientationAlign.homo['bad'], dataset.orientationAlign.bi['bad']]
        }, {
            name: 'Neutral',
            color: Highcharts.getOptions().colors[2],
            data: [dataset.orientationAlign.hetero['neutral'], dataset.orientationAlign.homo['neutral'], dataset.orientationAlign.bi['neutral']]
        }, {
            name: 'Good',
            color: Highcharts.getOptions().colors[0],
            data: [dataset.orientationAlign.hetero['good'], dataset.orientationAlign.homo['good'], dataset.orientationAlign.bi['good']]
        }]
    });

    ResetOptions();
    $('.scatterPlot').highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: 'Ratio of Public Identity Versus Ratio of Good Characters by Year'
        },
        subtitle: {
            text: 'Comic Characters from 1935 to 2013'
        },
        xAxis: {
            title: {
                enabled: true,
                text: 'Good Character (%)'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true,
            max: 1
        },
        yAxis: {
            title: {
                text: 'Public Identity (%)'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor:'#EEEEEE',
            borderWidth: 1
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<p style="display:none"></p>',
                    pointFormat: '<b>{point.year}</b><br>{point.x:.2f}, {point.y:.2f}'
                }
            }
        },
        series: [{
            name: 'Year',
            color: 'rgba(223, 83, 83, .5)',
            data: dataset.scatterPlotData
        }]
    });

    Highcharts.setOptions(Highcharts.theme);
    $('.pie1').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Alignment of Female Characters'
        },
        tooltip: {
            pointFormat: '<b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        fontSize: '1.4em'
                    }
                }
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            data: [
                {
                    name: 'Good',
                    y: dataset.alignPieData.goodFemale,
                },
                ['Neutral', dataset.alignPieData.neutralFemale],
                {
                    name: 'Bad',
                    y: dataset.alignPieData.badFemale,
                    color: 'red'
                }
            ]
        }]
    });

    $('.pie2').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Alignment of Male Characters'
        },
        tooltip: {
            pointFormat: '<b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        fontSize: '1.4em'
                    }
                }
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            data: [
                {
                    name: 'Good',
                    y: dataset.alignPieData.goodMale,
                },
                ['Neutral', dataset.alignPieData.neutralMale],
                {
                    name: 'Bad',
                    y: dataset.alignPieData.badMale,
                    color: 'red'
                }
            ]
        }]
    });
});