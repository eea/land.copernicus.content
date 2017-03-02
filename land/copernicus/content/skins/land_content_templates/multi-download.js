$(document).ready(function() {
  // [TODO] Send the GA custom event for each file

  var files = files_str.split(',');
  multiDownload(files);
});
