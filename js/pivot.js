function submit() {
    //Submit button generates a pivot table
    var tablehtml = '';
    var row = $('#row option:selected').val();
    var column = $('#column option:selected').val();
    var value = $('#value option:selected').val();
    var filterValues = $('#tokenize').val();
    $.ajax({
        type: "POST",
        data: {row: row, column: column, value: value, filterValues: filterValues, wantFilter: "False"},
        dataType: 'html',
        url: 'pivot.py',
        success: function(data) {
          $('#table').html(data);
        }
    });

    return false;
}

function filterChange() {
    //Changes the filter options depending on which column data is selected
    var column = $('#column option:selected').val();
    var value = $('#value option:selected').val();
    var filter = $('#filter option:selected').val();
    var row = $('#row option:selected').val();
    var filterValues = $('#tokenize').val();
    list = '';
    list += '<select id="tokenize" multiple="multiple" class="filterSelect">'
    $.ajax({
        type: "GET",
        data: {row: row, column: column, value: value, filterValues: filterValues, wantFilter: "True"},
        dataType: 'json',
        url: 'pivot.py',
        success: function(columns) {
            for (var j = 0; j < columns.length; j++){
                list += "<option value='" +columns[j] + "'>" +columns[j]+ "</option>";
            }
        }
    });
    $(document).ajaxStop(function () {
        list += '</select>';
        $('.filtering').html(list);
        $('#tokenize').tokenize({displayDropdownOnFocus:true, nbDropdownElements: 30});
    });
}

$(document).ready(function() {
    filterChange();
    $('#generate').click(submit);
    $("#column").change(filterChange);
});