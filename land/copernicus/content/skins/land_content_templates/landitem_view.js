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
  if (isNaN(parseFloat(data)) === true) {
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

$(document).ready(function() {

  function user_seems_to_be_anonymous() {
    /* Used only to prevent opening multiple unnecessary login tabs. */
    return $("#personaltools-login").length === 1;
  }

  function is_validated_dataset() {
    /* Returns true if validated dataset */
    return $("#checkbox-accept-non-validated").length === 0;
  }

  function add_not_validated_tag() {
    /* Add a custom or default text for not validated dataset after title */
    $("#parent-fieldname-title").css("display", "inline");
    var not_validated_text = $("#not-validated-custom-text").text();
    $("#not-validated-custom-text").hide();
    if(not_validated_text.length < 5) {
      not_validated_text = "Not yet validated.";
    }
    $("#parent-fieldname-title").after("<div class='not-validated-container'><span class='not-validated-tag'>" + not_validated_text + "</span></div>");

    // Fix print button position problem
    $(".printButton").css({"position": "relative", "top": "-50px"});
  }

  function disable_download_buttons() {
    /* Disable download, download selected and download all buttons */
    $("#button-download-selected").attr("disabled", "disabled");
    $("#button-download-all").attr("disabled", "disabled");
    $(".download-button").addClass("disabled");
  }

  function enable_download_buttons() {
    /* Enable download, download selected and download all buttons */
    $("#button-download-selected").removeAttr("disabled");
    $("#button-download-all").removeAttr("disabled");
    $(".download-button").removeClass("disabled");
  }

  function get_number_checked_items() {
    /* Count checked files for download */
    var number_checked = $('.checkbox-select-item:checked').size();
    return number_checked;
  }

  function check_all_items() {
    /* Prepare download all */
    $('.checkbox-select-item').prop('checked', true);
  }

  function uncheck_all_items() {
    /* Reset selected files for download */
    $('.checkbox-select-item').prop('checked', false);
  }

  function refresh_counter() {
    /* Refresh counter in download selected button */
    $("#number-checked").text(get_number_checked_items());
  }

  function save_selected_items_in_url() {
    /* For after login. Download tab is opened and these items will be checked automatically. */
    var selected = "?selected=";
    $('.checkbox-select-item').each(function(i) {
      if(this.checked) {
        selected += '@' + this.getAttribute("item_id");
      }
    });

    $('.download-button').each(function() {
      var old_href = $(this).attr("href");
      $(this).attr("href", old_href + selected);
    });
  }

  function button_click(button) {
    /* Open button href in a new tab */
    if(button.click) {
      button.click();
    } else {
      /* Used instead of button.click() to solve Safari problem:
      TypeError: 'undefined' is not a function (evaluating 'button.click()') */
      window.open($(button).attr("href"), '_blank');
    }
  }

  function redirect_click(button) {
    /* Redirect to button href. Works on Safari, too. */
    var click_event = document.createEvent("MouseEvents");
    click_event.initEvent("click", true /* bubble */, true /* cancelable */);
    button.dispatchEvent(click_event);
  }

  function download_all() {
    /* Start download all files */
    check_all_items();
    save_selected_items_in_url();
    var anon = user_seems_to_be_anonymous();
    var download_buttons = $('.download-button');
    for(var i = 0; i < download_buttons.length; i++) {
      var button = download_buttons[i];
      if(anon){
        /* A single login tab is neccessary. */
        button.removeAttribute("target");
        redirect_click(button);
        break;
      } else {
        button_click(button);
      }
    }
  }

  function download_selected() {
    /* Start download selected files */
    save_selected_items_in_url();
    var anon = user_seems_to_be_anonymous();
    var download_buttons = $('.checkbox-select-item:checked')
                           .closest('tr').find('.download-button');

    for(var i = 0; i < download_buttons.length; i++) {
      var button = download_buttons[i];
      if(anon) {
        /* A single login tab is neccessary. */
        button.removeAttribute("target");
        redirect_click(button);
        break;
      } else {
        button_click(button);
      }
    }
  }

  function auto_accept_not_validated() {
    /* User already checked it before login */
    $("#checkbox-accept-non-validated").prop("checked", true);
    enable_download_buttons();
  }

  function auto_select_checkboxes(checkboxes_indexes_array) {
    /* Prepare auto download after login */
    $('.checkbox-select-item').each(function(i) {
      var item_id = this.getAttribute("item_id");
      if($.inArray(item_id.toString(), checkboxes_indexes_array) != -1) {
        $(this).prop("checked", true);
      }
    });
  }

  function display_portal_message(message_text, message_type) {
    /* Display message at the top */
    $('<dl class="portalMessage ' + message_type + '"><dt>Error</dt><dd>' +
      message_text + '</dd></dl>').insertBefore('.documentFirstHeading');
  }

  function display_errors_if_any(download_tab_param) {
  // Example: ?fieldsetlegend-download=true-error-not-found-LandFile3
  // -> "LandFile3 cannot be downloaded. Broken link."
    var error_missing_file = "true-error-not-found-";
    if (download_tab_param.indexOf(error_missing_file) >= 0) {
      var land_file_title = download_tab_param.substring(error_missing_file.length, download_tab_param.length);
      if (land_file_title.length === 0) {
        land_file_title = "This land file";
      }

      display_portal_message(decodeURI(land_file_title) + " cannot be downloaded. Link is broken.", "error");
    }

  // Example: ?fieldsetlegend-download=true-error-profile-not-complete
  // -> "You can't download files until you update your profile with missing thematic and institutional domain info."
    error_missing_file = "true-error-profile-not-complete";

    if (download_tab_param.indexOf(error_missing_file) >= 0) {
      display_portal_message("You can't download files until you <a href=" + portal_url + "/@@personal-information" + "><b>update your profile</b></a> with missing thematic and institutional domain info.", "error");
    }
  }

  function download_auto_selected(download_tab_param) {
  // Example in URL: fieldsetlegend-download=true-selected-@clc_2006@landitem_new => autoselected by id
  // "clc_2006" and "landitem_new" land items
    var auto_selected_checkboxes_indexes = download_tab_param.split("@");
    auto_select_checkboxes(auto_selected_checkboxes_indexes);
    refresh_counter();
    auto_accept_not_validated();
    download_selected();
  }

  function interpret_url_params_if_any() {
  // Check parameter in url for after login case or error missing land file
  // Auto open download tab and download if any auto selected.

    function get_url_parameter(sParam) {
        var sPageURL = window.location.search.substring(1);
        var sURLVariables = sPageURL.split('&');
        for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == sParam) {
                return sParameterName[1];
            }
        }
    }

    var download_tab_param = get_url_parameter('fieldsetlegend-download');
    if (download_tab_param !== undefined) {
      $("#fieldsetlegend-download").click();
      download_auto_selected(download_tab_param);
      display_errors_if_any(download_tab_param);
    }
  }

  function replace_missing_or_fix_short() {
    /* Hide empty datatable or fix its height for less content. */
    var number_of_items = $('.checkbox-select-item').length;

    if(number_of_items < 10) {
      if(number_of_items === 0) {
        $("#datatable-container").hide();
        $("#disclaimer-download-container").hide();
      } else {

        /* Fix table height */
        var table_height = number_of_items * 50 + 10;
        $('.dataTables_scrollBody').css('height', table_height);
      }
    }
  }

  function fix_badges_for_both_raster_vector() {
    /* If a file in datatable has both types raster and vector we fix badge design here. */
    $('span.vector-raster, span.raster-vector').each(function() {
      $(this).html("<span class='raster'>Raster</span> <span class='vector'>Vector</span>");
    });
  }

  function init_disabled_buttons_behaviour() {
    /* If a disabled download button is clicked focus checkbox to accept not validated */
    $(".download-button.disabled").on("click", function() {
      $("#checkbox-accept-non-validated").focus();
      $('#text-accept-non-validated').animate({backgroundColor: '#FDA42C'}, 'slow');
      $('#text-accept-non-validated').animate({backgroundColor: '#fff'}, 'slow');
    });
  }

  // INIT
  if (!is_validated_dataset()) {
    disable_download_buttons();
    init_disabled_buttons_behaviour();
    add_not_validated_tag();
  } else {
    enable_download_buttons();
    $("#not-validated-custom-text").hide();
  }

  interpret_url_params_if_any();  // set by RedirectDownloadUrl class

  $('#data-table-download').dataTable({
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
    ],
    "scrollY": "500px",
    "scrollCollapse": true,
    "paging": false
  });

  replace_missing_or_fix_short();
  fix_badges_for_both_raster_vector();

  // tr hover
  $('.download-button').hide();
  $('#data-table-download > tbody > tr').on("mouseenter", function() {
    $(this).find('a.download-button').show();
    $(this).find('.download-gray-icon').hide();
  });

  $('#data-table-download > tbody > tr').on("mouseleave", function() {
    $(this).find('a.download-button').hide();
    $(this).find('.download-gray-icon').show();
  });

  // accept (un)checked
  $("#checkbox-accept-non-validated").change(function() {
    if(this.checked) {
      enable_download_buttons();
    } else {
      disable_download_buttons();
    }
  });

  // item (un)checked
  $(".checkbox-select-item").change(function() {
    refresh_counter();
  });

  // (un)select all items
  $(".checkbox-select-all").change(function() {
    if(this.checked) {
      check_all_items();
    } else {
      uncheck_all_items();
    }
    refresh_counter();
  });

  // DOWNLOAD
  $('#button-download-selected').on("click", function(evt) {
    evt.preventDefault();
    download_selected();
  });

  $('#button-download-all').on("click", function(evt) {
    evt.preventDefault();
    download_all();
  });

  $('.download-button').on("click", function(evt) {
    if($(this).hasClass("disabled")) {
      evt.preventDefault();
    } else {
      var anon = user_seems_to_be_anonymous();
      if(anon) {
        /* A single login tab is neccessary. */
        this.removeAttribute("target");
      }
      uncheck_all_items();
      $(this).parent().parent().find('.checkbox-select-item').prop("checked", true);
      save_selected_items_in_url();
    }
  });
});
