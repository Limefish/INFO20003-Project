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
        url: '../Pivot Table/pivot.py',
        success: function(data) {
          console.log(data)
          $('#testTitle').html(data);
        }
    });

    return false;
}

$(document).ready(
    function Init() {
      $('#generate').click(submit);
    }
);