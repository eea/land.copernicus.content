webpackJsonp([1],{"0e2k":function(t,e){},NHnr:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var s=i("7+uW"),n={render:function(){var t=this.$createElement;return(this._self._c||t)("div",{staticClass:"editable-div",attrs:{contenteditable:"true"},on:{blur:this.emit_change}},[this._v(this._s(this.content))])},staticRenderFns:[]};var o=i("VU/8")({name:"editable",props:["content"],methods:{emit_change:function(t){this.$emit("update",t.target.textContent)}}},n,!1,function(t){i("0e2k")},"data-v-2646d6a0",null).exports,l={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("select",{on:{change:function(e){t.update_selected_file()}}},[i("option"),t._v(" "),t._l(this.$parent.files,function(e){return i("option",[t._v(t._s(e))])})],2)},staticRenderFns:[]},r=i("VU/8")({name:"fileselect",props:["content","index_row","index_col"],methods:{update_selected_file:function(t){var e=this.$el.value;this.$parent.update_row(e,this.index_row,this.index_col)}}},l,!1,null,null,null).exports,a=i("mvHQ"),c=i.n(a),d={name:"tablepreview",props:["content"],methods:{export_json:function(){var t=this.$parent.columns,e=this.$parent.rows,i=this.$parent.filters,s=c()({columns:t,rows:e,filters:i});$("#exported-json").text(s)},save_work:function(){this.export_json(),$("form#save-work").submit()},cancel_work:function(){window.location.href="./"},upload_files:function(){this.$parent.files.push("newuploadedfile1","newuploadedfile2","newuploadedfile3")},render_table:function(){var t=this.$parent.columns,e=this.$parent.rows,i=this.$parent.filters,s=document.querySelector(".table-render-preview");$.fn.DataTable.isDataTable(".table-render-preview")&&$(".table-render-preview").DataTable().clear().destroy();var n=document.createElement("table");n.className="table-render-preview",n.innerHTML=function(t,e){function i(t){if(void 0!==t){var e=document.location.href;return"<a href='"+e.substring(0,e.lastIndexOf("/"))+"/"+t+"' target='_blank' title="+t+">File<span style='display:none !important'>"+t+"</span></a>"}return"N/A"}for(var s,n="<table border=1><thead><tr>",o=0;o<t.length;o++)n+="<th>"+t[o].text+"</th>";for(n+="</thead><tbody>",o=0;o<e.length;o++){n+="<tr>";for(var l=0;l<e[o].length;l++)"URL"==t[l].text||"URL"==t[l].text.trim()?n+="<td>"+(void 0!==(s=e[o][l].text)?"<a href='"+s+"' target='_blank' title="+s+">Link<span style='display:none !important'>"+s+"</span></a>":"N/A")+"</td>":"File"==t[l].text||"File"==t[l].text.trim()?n+="<td>"+i(e[o][l].text)+"</td>":n+="<td>"+e[o][l].text+"</td>";n+="</tr>"}return n+="</tbody></table>"}(t,e),s.parentNode.replaceChild(n,s);var o=$(".table-render-preview").dataTable({destroy:!0,aaSorting:[]});$(".dataTables_wrapper").append(function(t){for(var e="<div class='filters-container'><p><b>Search filters:</b></p><ul class='filters-list'>",i=0;i<t.length;i++)e+="<li class='search-filter'>"+t[i].text+"</li>";return e+="</ul></div>"}(i)),$(".search-filter").on("click",function(){o.fnFilter('"'+$(this).text()+'"'),$(".search-filter").removeClass("is-selected"),$(this).addClass("is-selected")})}}},f={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"table-preview-container"},[i("button",{staticClass:"large-btn",attrs:{name:"save-work"},on:{click:t.save_work}},[t._v("Save")]),t._v(" "),i("button",{staticClass:"large-btn",attrs:{name:"render-table"},on:{click:t.render_table}},[t._v("Preview table")]),t._v(" "),i("button",{staticClass:"large-btn",attrs:{name:"upload-files"},on:{click:t.upload_files}},[t._v("Upload files")]),t._v(" "),i("button",{staticClass:"large-btn",attrs:{name:"cancel-work",title:"The unsaved work will be lost."},on:{click:t.cancel_work}},[t._v("Cancel")]),t._v(" "),i("table",{staticClass:"table-render-preview"})])},staticRenderFns:[]};var u=i("VU/8")(d,f,!1,function(t){i("xQGC")},"data-v-71ec4e60",null).exports,_=i("mtWM"),h=i.n(_),m={name:"filesupload",data:function(){return{file:""}},methods:{handle_file_upload:function(){this.file=this.$refs.file.files[0]},submit_file:function(){var t=new FormData;t.append("file",this.file),h.a.post("./admin_files_library",t,{headers:{"Content-Type":"multipart/form-data"}}).then(function(){console.log("SUCCESS!!")}).catch(function(){console.log("FAILURE!!")})}}},w={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"form-container"},[i("form",{ref:"files_upload_form",staticClass:"files-upload-form",attrs:{action:"./admin_files_library",method:"post",enctype:"multipart/form-data"}},[i("label",[t._v("File")]),t._v(" "),i("input",{ref:"file",attrs:{type:"file",id:"file",name:"file"},on:{change:function(e){t.handle_file_upload()}}}),t._v(" "),i("button",{on:{click:function(e){t.submit_file()}}},[t._v("Upload")])])])},staticRenderFns:[]},p={name:"app",components:{editable:o,fileselect:r,tablepreview:u,filesupload:i("VU/8")(m,w,!1,null,null,null).exports},data:function(){return{LOREM:"Click me to edit",NONE:"",IS_DEBUG_MODE:!1,filters:this.get_filters(),columns:this.get_columns(),rows:this.get_rows(),files:this.get_files()}},methods:{generate_random:function(t,e){return Math.random()*(e-t)+t},get_initial_json_data:function(){var t=$("#initial-json-data").text();try{return JSON.parse(t)}catch(t){return{}}},get_files:function(){var t=$("#initial-existing-files-in-context").text();try{return JSON.parse(t)}catch(t){return["filename1","filename2","filename3"]}},file_exists:function(t){return this.files.indexOf(t)>-1},get_filters:function(){var t=this.get_initial_json_data();return t.filters?t.filters:[{id:"filter01",text:"Demo category"},{id:"filter02",text:"Demo category 2"},{id:"filter02",text:"Sub-category 3"}]},get_columns:function(){var t=this.get_initial_json_data();return t.columns?t.columns:[{id:"001",text:"Click me to edit"},{id:"002",text:"Demo column 2"},{id:"003",text:"Demo column 3"},{id:"004",text:"URL"},{id:"005",text:"File"}]},get_rows:function(){var t=this.get_initial_json_data();return t.rows?t.rows:[[{id:"005",text:"Demo category"},{id:"006",text:"Sub-category 1"},{id:"007",text:"col3 data1"},{id:"008",text:"https://www.google.com"},{id:"111",text:"File title1"}],[{id:"009",text:"Demo category"},{id:"010",text:"Sub-category 2"},{id:"011",text:"col3 data2"},{id:"012",text:"https://www.yahoo.com"},{id:"111",text:"File title2"}]]},is_url_col:function(t){return"URL"==t},is_file_col:function(t){return"File"==t},is_editable_col:function(t){return!(this.is_url_col(t)||this.is_file_col(t))},generate_id:function(){return"__key_prefix__"+Date.now()+"_"+this.generate_random(1e4,99999)},new_data:function(t){return{id:this.generate_id(),text:t}},refresh:function(){for(var t=0;t<this.columns.length;t++)this.columns[t].id=this.generate_id();for(t=0;t<this.rows.length;t++)for(var e=0;e<this.columns.length;e++)this.rows[t][e].id=this.generate_id();this.$forceUpdate()},update_col:function(t,e){this.columns[e].text=t.trim(),this.refresh()},update_row:function(t,e,i){this.rows[e][i].text=t.trim(),this.refresh()},add_col:function(t){this.columns.splice(t,0,this.new_data(this.LOREM));for(var e=0;e<this.rows.length;e++){this.rows[e].splice(t,0,this.new_data(this.NONE))}this.refresh()},delete_col:function(t){if(!(arguments.length>1&&void 0!==arguments[1]&&arguments[1])&&!confirm("Are you sure you want to delete this column?"))return;this.columns.splice(t,1);for(var e=0;e<this.rows.length;e++){this.rows[e].splice(t,1)}this.refresh()},add_row:function(t){this.rows.splice(t,0,new Array(this.columns.length));for(var e=0;e<this.columns.length;e++)this.rows[t][e]=this.new_data(this.NONE);this.refresh()},delete_row:function(t){if(!(arguments.length>1&&void 0!==arguments[1]&&arguments[1])&&!confirm("Are you sure you want to delete this row?"))return;this.rows.splice(t,1),this.refresh()},delete_all_rows:function(){if(confirm("Are you sure you want to delete all rows?")){for(var t=this.rows.length,e=0;e<t;e++)this.delete_row(0,!0);this.refresh()}},delete_all_cols:function(){if(confirm("Are you sure you want to delete all columns?")){for(var t=this.columns.length,e=0;e<t;e++)this.delete_col(0,!0);this.refresh()}},move_col_to_left:function(t){if(0!=t){var e=this.columns[t-1].text;this.columns[t-1].text=this.columns[t].text,this.columns[t].text=e;for(var i=0;i<this.rows.length;i++)e=this.rows[i][t-1].text,this.rows[i][t-1].text=this.rows[i][t].text,this.rows[i][t].text=e;this.columns=this.columns.slice(),this.rows=this.rows.slice(),this.refresh()}},move_col_to_right:function(t){if(t!=this.columns.length-1){var e=this.columns[t+1].text;this.columns[t+1].text=this.columns[t].text,this.columns[t].text=e;for(var i=0;i<this.rows.length;i++)e=this.rows[i][t+1].text,this.rows[i][t+1].text=this.rows[i][t].text,this.rows[i][t].text=e;this.columns=this.columns.slice(),this.rows=this.rows.slice(),this.refresh()}},move_row_up:function(t){if(0!=t){var e=this.rows[t-1];this.rows[t-1]=this.rows[t],this.rows[t]=e,this.columns=this.columns.slice(),this.rows=this.rows.slice(),this.refresh()}},move_row_down:function(t){if(t!=this.rows.length-1){var e=this.rows[t+1];this.rows[t+1]=this.rows[t],this.rows[t]=e,this.columns=this.columns.slice(),this.rows=this.rows.slice(),this.refresh()}}}},v={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{attrs:{id:"datatables-admin"}},[i("div",{staticStyle:{display:"none"},attrs:{id:"initial-json-data"}},[t._v('{"columns":[{"id":"001","text":"Click me to edit"},{"id":"002","text":"Demo column 2"},{"id":"003","text":"Demo column 3"},{"id":"004","text":"URL"}],"rows":[[{"id":"005","text":"Demo category"},{"id":"006","text":"Sub-category 1"},{"id":"007","text":"col3 data1"},{"id":"008","text":"https://www.google.com"}],[{"id":"009","text":"Demo category"},{"id":"010","text":"Sub-category 2"},{"id":"011","text":"col3 data2"},{"id":"012","text":"https://www.yahoo.com"}],[{"id":"013","text":"Demo category 2"},{"id":"014","text":"Sub-category 3"},{"id":"015","text":"col3 data3"},{"id":"016","text":"https://www.yahoo.com"}]],"filters":[{"id":"filter01","text":"Demo category"},{"id":"filter02","text":"Demo category 2"},{"id":"filter02","text":"Sub-category 3"}]}')]),t._v(" "),i("div",{staticStyle:{display:"none"},attrs:{id:"initial-existing-files-in-context"}},[t._v('["existingfile1", "existingfile2"]')]),t._v(" "),i("table",{attrs:{id:"editor"}},[i("thead",[i("tr",[t._l(t.columns,function(e,s){return i("th",{key:e.id},[i("i",{staticClass:"fa fa-arrow-left fa-2x dta-btn move-col-left",attrs:{title:"Move column to left"},on:{click:function(e){t.move_col_to_left(s)}}}),t._v(" "),i("i",{staticClass:"fa fa-arrow-right fa-2x dta-btn move-col-right",attrs:{title:"Move column to right"},on:{click:function(e){t.move_col_to_right(s)}}}),t._v(" "),i("i",{staticClass:"fa fa-plus fa-2x dta-btn add-col",attrs:{title:"Add a column after this one"},on:{click:function(e){t.add_col(s+1)}}}),t._v(" "),t.is_editable_col(t.columns[s].text)?i("i",{staticClass:"fa fa-times fa-2x dta-btn delete-col",attrs:{title:"Delete this column"},on:{click:function(e){t.delete_col(s)}}}):t._e(),t._v(" "),i("br"),t._v(" "),t.is_editable_col(t.columns[s].text)?i("editable",{attrs:{content:t.columns[s].text},on:{update:function(e){t.update_col(e,s)}}}):t._e(),t._v(" "),t.is_editable_col(t.columns[s].text)?t._e():i("span",{staticClass:"not-editable"},[t._v(t._s(t.columns[s].text))])],1)}),t._v(" "),i("th",[i("i",{staticClass:"fa fa-plus fa-2x dta-btn add-col",attrs:{title:"Add a column"},on:{click:function(e){t.add_col(0)}}}),t._v(" "),i("i",{staticClass:"fa fa-plus fa-2x dta-btn add-row",attrs:{title:"Add a row"},on:{click:function(e){t.add_row(0)}}}),t._v(" "),i("i",{staticClass:"fa fa-times fa-2x dta-btn delete-all-cols",attrs:{title:"Delete all columns"},on:{click:t.delete_all_cols}}),t._v(" "),i("i",{staticClass:"fa fa-times fa-2x dta-btn delete-all-rows",attrs:{title:"Delete all rows"},on:{click:t.delete_all_rows}})])],2)]),t._v(" "),i("tbody",t._l(t.rows,function(e,s){return i("tr",{key:s},[t._l(t.columns,function(e,n){return i("td",{key:e.id},[t.is_file_col(t.columns[n].text)?t._e():i("editable",{attrs:{content:t.rows[s][n].text},on:{update:function(e){t.update_row(e,s,n)}}}),t._v(" "),t.is_file_col(t.columns[n].text)?i("span",{staticClass:"not-editable"},[t._v("\n            "+t._s(t.rows[s][n].text)+"\n\n            "),t.file_exists(t.rows[s][n].text)?t._e():i("span",{staticClass:"missing-file",attrs:{title:"This file seems missing in current folder."}},[t._v("\n                (missing)\n            ")])]):t._e(),t._v(" "),t.is_file_col(t.columns[n].text)?i("fileselect",{attrs:{content:t.rows[s][n].text,index_row:s,index_col:n}}):t._e()],1)}),i("td",[i("i",{staticClass:"fa fa-arrow-up fa-2x dta-btn move-row-up",attrs:{title:"Move row up"},on:{click:function(e){t.move_row_up(s)}}}),t._v(" "),i("i",{staticClass:"fa fa-arrow-down fa-2x dta-btn move-row-down",attrs:{title:"Move row down"},on:{click:function(e){t.move_row_down(s)}}}),t._v(" "),i("i",{staticClass:"fa fa-plus fa-2x dta-btn add-row",attrs:{title:"Add a row under this one"},on:{click:function(e){t.add_row(s+1)}}}),t._v(" "),i("i",{staticClass:"fa fa-times fa-2x dta-btn delete-row",attrs:{title:"Delete this row"},on:{click:function(e){t.delete_row(s)}}})])],2)}))]),t._v(" "),t.IS_DEBUG_MODE?i("div",[i("p",[i("b",[t._v("Columns:")]),t._v(" "),i("span",{domProps:{textContent:t._s(t.columns)}})]),t._v(" "),i("p",[i("b",[t._v("Rows:")]),t._v(" "),i("span",{domProps:{textContent:t._s(t.rows)}})])]):t._e(),t._v(" "),t._m(0),t._v(" "),i("filesupload"),t._v(" "),i("tablepreview")],1)},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("form",{staticStyle:{display:"none"},attrs:{id:"save-work",action:"./admin_files_library",method:"post"}},[e("textarea",{attrs:{id:"exported-json",name:"exported-json"}},[this._v("JSON PLACEHOLDER")])])}]};var x=i("VU/8")(p,v,!1,function(t){i("jJLA")},null,null).exports;s.a.config.productionTip=!1,new s.a({el:"#datatables-admin",template:"<App/>",components:{App:x}})},jJLA:function(t,e){},xQGC:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.js.map