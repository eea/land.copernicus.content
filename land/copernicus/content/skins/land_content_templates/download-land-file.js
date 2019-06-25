$(document).ready(function() {

  function get_browser_info() {
    /* Return browser name and version */
    var ua=navigator.userAgent,tem,M=ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
    if(/trident/i.test(M[1])) {
      tem=/\brv[ :]+(\d+)/g.exec(ua) || [];
      return {name:'IE',version:(tem[1]||'')};
    }

    if(M[1]==='Chrome') {
      tem=ua.match(/\bOPR\/(\d+)/);
      if(tem!==null)   {return {name:'Opera', version:tem[1]};}
    }

    M=M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];

    if((tem=ua.match(/version\/(\d+)/i))!==null) {
      M.splice(1,1,tem[1]);
    }

    return {
      name: M[0],
      version: M[1]
    };
  }

  // Custom dimensions
  ga('set', 'dimension1', professional_thematic_domain);
  ga('set', 'dimension2', institutional_domain);
  ga('set', 'dimension3', is_eionet_member);

  // Track event
  ga('send', {
    'hitType': 'event',                 // Required.
    'eventCategory': 'page',            // Required.
    'eventAction': 'landfile_download', // Required.
    'eventLabel': land_item_title,
    'eventValue': 1
  });

  var user_browser = get_browser_info().name;
  if(user_browser != "Safari") {
    // Start download the file and close the tab
    var newTab = window.open(start_download_url, "_blank");
    window.top.close();
  } else {
    // For Safari we use invisible iframe to download the file.
    // Auto close new tab not possible
    $("#download-iframe").attr("src", start_download_url);
  }
});
