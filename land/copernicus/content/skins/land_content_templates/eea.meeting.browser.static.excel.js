window.saveFile = function saveFile (selector, title, json_opts) {
    var table = $(selector).tableToJSON(json_opts);


    if(selector == '#subscribers'){
        table.forEach(function(item){
            delete item['User Name'];
        });
    }

    var opts = [{sheetid:'Sheet 1',header:true}];
    var res = alasql('SELECT * INTO XLSX("Export_'+title+'.xls",?) FROM ?',
                     [opts,[table]]);
};
