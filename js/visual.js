var dataset

$(document).ready(function() {
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
    $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: 'Alignment of Female Characters'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'Browser share',
            data: [
                {
                    name: 'Good',
                    y: dataset.alignPieData.goodFemale,
                    sliced: true,
                    selected: true
                },
                ['Neutral', dataset.alignPieData.neutralFemale],
                ['Bad', dataset.alignPieData.badFemale],
                ['Reformed', dataset.alignPieData.reformedFemale],
                ['NotAvailable', dataset.alignPieData.notAvailable]
            ]
        }]
    });
});