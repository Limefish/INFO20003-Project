function submit() {
    var tablehtml = '';
    var row = $('#row option:selected').val();
    var column = $('#column option:selected').val();
    var value = $('#value option:selected').val();
    var filter = $('#filter option:selected').val();
    var filterValue = $('#filterValue').val();
    $.ajax({
        type: "POST",
        data: {row: row, column: column, value: value, filter: filter, filterValue: filterValue},
        dataType: 'html',
        url: 'pivot.py',
        success: function(data) {
          console.log(data)
          $('#table').html(data);
        }
    });

    return false;
}

$(document).ready(function() {
    if ($('#filter option:selected').val() == "all") {
        $("#filterValue").css({
            'opacity': '0.3'
        });
    } else {
        $("#filterValue").css({
            'opacity': '1.0'
        });
    };
    $('#generate').click(submit);
    $("#filter").change(function() {
        if($('#filter option:selected').val() == "all") {
            $("#filterValue").prop("disabled", true)
            $("#filterValue").css({
                'opacity': '0.3'
            });
        } else {
            $("#filterValue").prop("disabled", false)
            $("#filterValue").css({
                'opacity': '1.0'
            });
        }
    });
});