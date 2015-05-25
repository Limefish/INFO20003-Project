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
      
    var femaleValues = []
    var maleValues = []
    var femaleCount = {};
    var maleCount = {};
    var totalCount = {};

    //Sorts the sbjects by Year (if required)
    Object.keys(dataset.femaleCount)
          .sort()
          .forEach(function (year) {
             femaleCount[year] = dataset.femaleCount[year];
          });
    Object.keys(dataset.maleCount)
          .sort()
          .forEach(function (year) {
             maleCount[year] = dataset.maleCount[year];
          });
    Object.keys(dataset.totalCount)
          .sort()
          .forEach(function (year) {
             totalCount[year] = dataset.totalCount[year];
          });
    

    //Makes sure that both males and females have the same amount of years
    for (var year in femaleCount) {
        femaleValues.push(femaleCount[year]/totalCount[year])
    }
    for (var year in maleCount) {
        maleValues.push(maleCount[year]/totalCount[year])
    }

    //Generation of Charts
    $('.genderRatio').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: 'Gender Ratio of Comic Book Characters Introduced Each Year'
        },
        subtitle: {
            text: 'Maybe add a line indicating the cumulative'
        },
        xAxis: {
            categories: Object.keys(maleCount),
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
            max: 1,
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
                    lineWidth: 1,
                    lineColor: '#666666'
                }
            }
        },
        series: [{
            name: 'Males',
            data: maleValues
        }, {
            name: 'Females',
            data: femaleValues
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
    
    $('.scatterPlot').highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: 'Ratio of Public Identity Versus Ratio of Good Characters'
        },
        subtitle: {
            text: 'Comic Characters from 1935 to 2013'
        },
        xAxis: {
            title: {
                enabled: true,
                text: 'Good Character Ratio (%)'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: 'Public Identity Ratio (%)'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
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
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: '{point.x} %, {point.y} %'
                }
            }
        },
        series: [{
            name: 'Year',
            color: 'rgba(223, 83, 83, .5)',
            data: dataset.scatterPlotData
        }]
    });

    ResetOptions();
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
});​