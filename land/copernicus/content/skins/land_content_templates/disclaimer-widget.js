$(function() {
  function show_first_page() {
    $("#terms-page1-container").show();
    $("#terms-page2-container").hide();
    $("#controls #prev-page").hide();
    $("#controls #next-page").show();
  }

  function show_second_page() {
    $("#terms-page1-container").hide();
    $("#terms-page2-container").show();
    $("#controls #prev-page").show();
    $("#controls #next-page").hide();
  }

  function init_pages() {
    $("#terms-source-container p").first().appendTo($("#terms-page1-container"));
    $("#terms-source-container p").first().appendTo($("#terms-page1-container"));
    $("#terms-source-container p").first().appendTo($("#terms-page1-container"));
    $("#terms-source-container").appendTo($("#terms-page2-container"));
  }

  function init_dialog() {
    var modal_width = $(window).width() - ($(window).width() / 3);
    var modal_height = $(window).height() - 50;

    $("#terms-of-use-modal").dialog({
      modal: true,
      width: modal_width,
      maxHeight: modal_height,
      dialogClass: 'terms-of-use-dialog',
      buttons: {
        Ok: function() {
          $(this).dialog("close");
        }
      }
    });
  }

  init_pages();

  $("#terms-of-use-link").on("click", function(evt) {
    evt.preventDefault();
    init_dialog();
    show_first_page();
  });

  $("#controls #prev-page").on("click", function(evt) {
    evt.preventDefault();
    show_first_page();
  });

  $("#controls #next-page").on("click", function(evt) {
    evt.preventDefault();
    show_second_page();
  });
});
