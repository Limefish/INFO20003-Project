var dataset

// Make a copy of the default theme
var HCDefaults = $.extend(true, {}, Highcharts.getOptions(), {});

function ResetOptions() {
    // Fortunately, Highcharts returns the reference to defaultOptions itself
    // We can manipulate this and delete all the properties
    var defaultOptions = Highcharts.getOptions();
    for (var prop in defaultOptions) {
        if (typeof defaultOptions[prop] !== 'function') delete defaultOptions[prop];
    }
    // Fall back to the defaults that we captured initially, this resets the theme
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
});