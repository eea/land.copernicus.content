/* This JS integrates the jQuery Tools Tooltips with the EEA site. */
jQuery(document).ready(function($) {
  if ($.fn.tooltip !== undefined) {
    // Inflexible tooltips
    $(".eea-tooltip-top").each(function(i) {
      var title = $(this).attr("title");
      $(this).tooltip({
        effect: 'fade',
        tipClass: 'eea-tooltip-markup-top'
      });
    });
    $(".eea-tooltip-bottom").each(function(i) {
      var title = $(this).attr("title");
      $(this).tooltip({
        effect: 'fade',
        position: 'bottom center',
        tipClass: 'eea-tooltip-markup-bottom'
      });
    });
    $(".eea-tooltip-left").each(function(i) {
      var title = $(this).attr("title");
      $(this).tooltip({
        effect: 'fade',
        position: 'center left',
        tipClass: 'eea-tooltip-markup-left'
      });
    });
    $(".eea-tooltip-right").each(function(i) {
      var title = $(this).attr("title");
      $(this).tooltip({
        effect: 'fade',
        position: 'center right',
        tipClass: 'eea-tooltip-markup-right'
      });
    });

    // Flexible tooltips
    var removeExtraText = function() {
      this.getTip()[0].lastChild.nodeValue = '';
    };

    $(".eea-flexible-tooltip-right").each(function(i){
      var title = $(this).attr("title");

      var container = $('<div>').addClass('eea-tooltip-markup');
      var bottomright = $('<div>').addClass('tooltip-box-br');
      var topleft = $('<div>').addClass('tooltip-box-tl');
      var content = $('<div>').addClass('tooltip-box-rcontent');
      content.text(title);

      topleft.append(content);
      bottomright.append(topleft);
      container.append(bottomright);

      $(this).tooltip({
        effect: 'fade',
        position: 'center right',
        offset: [20, 20],
        tipClass: 'eea-tooltip-markup',
        layout : container,
        onBeforeShow: removeExtraText
      });
    });

    $(".eea-flexible-tooltip-left").each(function(i){
      var title = $(this).attr("title");

      var container = $('<div>').addClass('eea-tooltip-markup');
      var bottomright = $('<div>').addClass('tooltip-box-br');
      var topleft = $('<div>').addClass('tooltip-box-tl');
      var content = $('<div>').addClass('tooltip-box-lcontent');
      content.text(title);

      topleft.append(content);
      bottomright.append(topleft);
      container.append(bottomright);

      $(this).tooltip({
        effect: 'fade',
        position: 'center left',
        offset: [20, -10],
        tipClass: 'eea-tooltip-markup',
        layout : container,
        onBeforeShow: removeExtraText
      });
    });

    $(".eea-flexible-tooltip-top").each(function(i){
      var title = $(this).attr("title");

      var container = $('<div>').addClass('eea-tooltip-markup');
      var bottomright = $('<div>').addClass('tooltip-box-br');
      var topleft = $('<div>').addClass('tooltip-box-tl');
      var content = $('<div>').addClass('tooltip-box-tcontent');
      content.text(title);

      topleft.append(content);
      bottomright.append(topleft);
      container.append(bottomright);

      $(this).tooltip({
        effect: 'fade',
        position: 'top center',
        offset: [10, 0],
        tipClass: 'eea-tooltip-markup',
        layout : container,
        onBeforeShow: removeExtraText
      });
    });

    $(".eea-flexible-tooltip-bottom").each(function(i){
      var title = $(this).attr("title");

      var container = $('<div>').addClass('eea-tooltip-markup');
      var bottomright = $('<div>').addClass('tooltip-box-br');
      var topleft = $('<div>').addClass('tooltip-box-tl');
      var content = $('<div>').addClass('tooltip-box-bcontent');
      content.text(title);

      topleft.append(content);
      bottomright.append(topleft);
      container.append(bottomright);

      $(this).tooltip({
        effect: 'fade',
        position: 'bottom center',
        offset: [30, 0],
        tipClass: 'eea-tooltip-markup',
        layout : container,
        onBeforeShow: removeExtraText
      });
    });
  }
});
