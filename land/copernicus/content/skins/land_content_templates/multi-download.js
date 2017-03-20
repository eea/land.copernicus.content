$(document).ready(function() {
  // [TODO] Send the GA custom event for each file

  var files = files_str.split(',');
  for (var index = 0; index < files.length; ++index) {
    var file = files[index];
    $.fileDownload(file)
      .done(function() {
        alert("Done " + file);
      }
    )
      .fail(function() {
        alert("Fail " + file);
      }
    );
  }
});
