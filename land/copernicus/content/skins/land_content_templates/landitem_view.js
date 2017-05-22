/**
* IMPORTANT: Don't use version on CDN for this plugin.
* This code used here was FIXED to work for NaN values like "N/A".
*
* When dealing with computer file sizes, it is common to append a post fix
* such as B, KB, MB or GB to a string in order to easily denote the order of
* magnitude of the file size. This plug-in allows sorting to take these
* indicates of size into account.
*
* A counterpart type detection plug-in is also available.
*
*  @name File size
*  @summary Sort abbreviated file sizes correctly (8MB, 4KB, etc)
*  @author Allan Jardine - datatables.net
*
*  @example
*    $('#example').DataTable( {
*       columnDefs: [
*         { type: 'file-size', targets: 0 }
*       ]
*    } );
*
*/

jQuery.fn.dataTable.ext.type.order['file-size-pre'] = function (data) {
  var units = data.replace(/[\d\.]/g, '').toLowerCase();
  var multiplier = 1;

  if (units === ' kb') {
    multiplier = 1000;
  } else if (units === ' mb') {
      multiplier = 1000000;
  } else if (units === ' gb') {
    multiplier = 1000000000;
  }
  if (isNaN(parseFloat(data)) == true) {
    return multiplier; // was "N/A", empty or some string.
  } else {
    return parseFloat(data) * multiplier;
  }
};

// This fixes sort alphabetically for special characters
jQuery.fn.dataTableExt.oSort['special-chars-sort-asc']  = function(a,b) {
  return a.localeCompare(b);
};
jQuery.fn.dataTableExt.oSort['special-chars-sort-desc']  = function(a,b) {
  return b.localeCompare(a);
};

(function(){

  var table = $('#data-table-download').dataTable({
    "order": [[ 1, "asc" ]],
    "columnDefs": [
      {
        "targets": 'no-sort',
        "orderable": false
      },
      {
        "targets": 0,
        "width": "20px"
      },
      {
        "targets": 'search-tags-hidden-column',
        "visible": false,
        "searchable": true
      },
      {
        "targets": 'file-size-column',
        "type": 'file-size'
      },
      {
        "targets": 'special-chars-sort',
        "type": 'special-chars-sort'
      }
    ]
  });

  table.$('td').on('click', function(){
    var role = this.getAttribute('data-role');
    var skip = ['checkbox', 'download'];
    if (skip.indexOf(role) === -1) {
      this.parentElement
        .querySelector('.checkbox-select-item')
        .click();
    }
  });

  table.$('.download-button').on('click', function(evt) {
    evt.preventDefault();
    var chk_accept = $("#checkbox-accept-non-validated");
    if (!chk_accept.checked) {
      chk_accept.focus();
      $('#text-accept-non-validated').fadeOut().fadeIn();
    }
  });

  table.$(".checkbox-select-item").change(function() {
    var selected = table.$('.checkbox-select-item:checked');
    $("[data-role='number-checked']").text(selected.length);
  });

  /* If a file in datatable has both types raster and vector we fix badge design here. */
  table.$('span.vector-raster, span.raster-vector').each(function() {
    $(this).html("<span class='raster'>Raster</span> <span class='vector'>Vector</span>");
  });

  // accept (un)checked
  $("#checkbox-accept-non-validated").change(function() {
    table.$(".download-button").toggleClass('disabled', !this.checked);
  });

})();
