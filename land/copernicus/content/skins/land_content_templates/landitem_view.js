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

  var TABLE = $('#data-table-download').dataTable({
    "pageLength": 20,
    "lengthMenu": [10, 20, 50, 100],
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


  var table_download_buttons = TABLE.$('.download-button');
  var table_checkboxes = TABLE.$(".checkbox-select-item");
  var elems_selected_counter = $("[data-role='number-checked']");
  var chk_accept = $("#checkbox-accept-non-validated");
  var elem_text_accept = $('#text-accept-non-validated');
  var elem_limit = $("[data-role='download-limit']");

  var FORM = $('#download-form');
  var LIMIT = parseInt(elem_limit.text(), 10);

  FORM.on('submit', function(evt) {
    evt.preventDefault();
    var selected = table_checkboxes.filter(':checked');
    console.log(selected.serialize() + '&' + FORM.serialize());
  });

  TABLE.$('td').on('click', function(){
    var role = this.getAttribute('data-role');
    var skip = ['checkbox', 'download'];
    if (skip.indexOf(role) === -1) {
      var chk = this.parentElement.querySelector('.checkbox-select-item');
      if (chk) {
        chk.click();
      }
    }
  });

  table_download_buttons.on('click', function(evt) {
    if (!chk_accept.is(':checked')) {
      evt.preventDefault();
      chk_accept.focus();
      elem_text_accept.fadeOut().fadeIn();
    }
  });

  table_checkboxes.change(function(evt) {
    var selected = table_checkboxes.filter(':checked');
    elems_selected_counter.text(selected.length);
    if (selected.length >= LIMIT) {
      table_checkboxes.filter(':not(:checked)').attr('disabled', 'disabled');
    }
    else {
      table_checkboxes.attr('disabled', null);
    }
  });

  /* If a file in datatable has both types raster and vector we fix badge design here. */
  TABLE.$('span.vector-raster, span.raster-vector').each(function() {
    $(this).html("<span class='raster'>Raster</span> <span class='vector'>Vector</span>");
  });

  // accept (un)checked
  chk_accept.change(function() {
    table_download_buttons.toggleClass('disabled', !this.checked);
  });

})();
