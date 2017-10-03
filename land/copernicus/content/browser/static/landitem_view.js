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
    multiplier = 1024;
  } else if (units === ' mb') {
      multiplier = 1048576;
  } else if (units === ' gb') {
    multiplier = 1073741824;
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

  var UNITS = {
    b: 1,
    kb: 1024,
    mb: Math.pow(1024, 2),
    gb: Math.pow(1024, 3)
  }

  // handle no GA code present.
  var ga = window.ga || function() {};


  function track_download(data) {
    // Custom dimensions
    ga('set', 'dimension1', data.thematic_domain);
    ga('set', 'dimension2', data.institutional_domain);
    ga('set', 'dimension3', data.is_eionet_member);

    // Track event
    ga('send', {
      'hitType': 'event',                 // Required.
      'eventCategory': 'page',            // Required.
      'eventAction': 'landfile_download', // Required.
      'eventLabel': data.land_item_title,
      'eventValue': 1
    });
  };

  function start_download(elem) {
    var remote_url = elem.data('href');
    $.ajax({
      url: remote_url,
      error: function(resp) {
        alert(resp.responseJSON.err);
      },
      success: function(resp) {
        console.log(resp);
        track_download(resp.ga);
        window.location.href = resp.url;
      }
    });
  }

  function _friendly_size(size) {
    var friendly = ['gb', 'mb', 'kb', 'b'].reduce(function(acc, unit){
      var value = parseInt(size / UNITS[unit], 10);
      return value > 0 && !acc ? {unit: unit.toUpperCase(), value: value} : acc;
    }, null)
    return friendly && friendly['value'] + ' ' + friendly['unit'] || null;
  }

  function update_filesize(container, target, elems) {
    var total = [].slice.call(elems).reduce(function(acc, elm){
      return acc + parseInt(elm.getAttribute('data-size'), 10);
    }, 0);
    if (total) {
      target.textContent = _friendly_size(total);
      container.style.display = '';
    } else {
      container.style.display = 'none';
    }
  }

  function update_selection(elem_size_display, elem_file_size, checkboxes) {
    var selected = checkboxes.filter(':checked');
    elems_selected_counter.text(selected.length);
    update_filesize(elem_size_display, elem_file_size, selected);
  }

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
  var elem_size_display = document.querySelector('[data-role="size-display"]');
  var elem_file_size = document.querySelector('[data-role="file-size"]');
  var chk_select_all = $(".checkbox-select-all");
  var chk_accept = $("#checkbox-accept-non-validated");
  var elem_text_accept = $('#text-accept-non-validated');

  var FORM = $('#download-form');

  FORM.on('submit', function(evt) {
    evt.preventDefault();
    var selected = table_checkboxes.filter(':checked');
    var payload = selected.serialize() + '&' + FORM.serialize();
    console.log(payload);
    document.location.href = document.location.href + '/@@download-land-files?' + payload;
  });

  TABLE.$('td').on('click', function(){
    var elem = $(this);
    var role = elem.data('role');
    var skip = ['checkbox', 'download'];
    if (skip.indexOf(role) === -1) {
      var chk = $('.checkbox-select-item', elem.parent());
      if (chk) {
        chk.click();
      }
    }
  });

  chk_select_all.on('change', function(evt){
    table_checkboxes.prop('checked', $(evt.target).is(':checked'));;
    update_selection(elem_size_display, elem_file_size, table_checkboxes);
  });


  table_download_buttons.on('click', function(evt) {
    evt.preventDefault();

    if (!chk_accept.is(':checked')) {
      chk_accept.focus();
      elem_text_accept.fadeOut().fadeIn();
    }
    else {
      start_download($(this));
    }
  });

  table_checkboxes.on('change', function() {
    update_selection(elem_size_display, elem_file_size, table_checkboxes);
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
