$(document).ready(function() {
  // [TODO] Send the GA custom event for each file

/*

 http://localhost:8081/copernicus/local/urban-atlas/urban-atlas-2012/@@redirect-download-url?selected=@barlad@tulcea@la-linea-de-la-concepcion@ceuta@alytus@aviles@torrevieja@santa-lucia-de-tirajana@alphen-aan-den-rijn@eastbourne@siauliai?selected=@barlad

?selected=
@barlad
@tulcea
@la-linea-de-la-concepcion
@ceuta@alytus
@aviles
@torrevieja
@santa-lucia-de-tirajana
@alphen-aan-den-rijn
@eastbourne@siauliai
?selected=@barlad

*/

  function download_file(url) {
    console.log("Downloading " + url)
    return $.fileDownload(url)
      .done(function() {
        alert("Done " + url); // remove this 100 alerts will be blocked by browser, maintain an array of files
      }
    )
      .fail(function() {
        alert("Fail " + url);
      }
    );
  }

  /* [TODO] Upgrade step to rewrite all these links or replace them in python code? */
  files_str = files_str.split("https://cws-download.eea.europa.eu").join("http://demo.copernicus.eea.europa.eu/filedownload");
  var files = files_str.split(',');
  var first_file = files[0];
  var download_result = download_file(first_file);

  var begin = 1;
  var end = 5;

  do {
    for (var index = 1; index < files.slice(begin, end).length; index++) {
      var file = files[index];
      (function (index) {
        download_result = download_result.then(function() {
          return download_file(file);
        });
      }(index));
    }
    index++;
    begin = begin + 5;
    end = end + 5;
  } while (end  < files.length);
});
