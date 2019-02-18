<template>
  <div class="table-preview-container">
    <button name="save-work" class='large-btn' v-on:click="save_work">Save</button>
    <button name="render-table" class='large-btn' v-on:click="render_table">Preview table</button>
    <button name="cancel-work" class='large-btn' title="The unsaved work will be lost." v-on:click="cancel_work">Cancel</button>
    <table class="table-render-preview"></table>
  </div>
</template>

<script>
export default {
  name: 'tablepreview',
  props: ['content'],
  methods: {
    export_json() {
      var columns = this.$parent.columns;
      var rows = this.$parent.rows;
      var filters = this.$parent.filters;
      var result = JSON.stringify({
        "columns": columns,
        "rows": rows,
        "filters": filters
      });

      $("#exported-json").text(result);
    },

    save_work() {
      this.export_json();
      $("form#save-work").submit();
    },

    cancel_work() {
      window.location.href = "./";
    },

    render_table() {
      var columns = this.$parent.columns;
      var rows = this.$parent.rows;
      var filters = this.$parent.filters;
      var table_placeholder = document.querySelector('.table-render-preview');

      function make_filters_html(filters) {
        var filters_html = "<div class='filters-container'><p><b>Filter by:</b></p><ul class='filters-list'>";
        for(var i = 0; i < filters.length; i++) {
          filters_html += "<li class='search-filter'>" + filters[i] + "</li>";
        }
        filters_html += "<li class='search-filter'>Show all</li>"
        filters_html += "</ul></div>"

        return filters_html;
      }

      function make_table_html(columns, rows) {
        function render_link(url) {
          if(url == "") {
            return "";
          }

          if(url !== undefined) {
            return "<a href='" + url +"' target='_blank' title=" + url + ">Link<span style='display:none !important'>" + url + "</span></a>";
          } else {
            return "N/A";
          }
        }

        function render_file(file_id) {
          if(file_id == "") {
            return "";
          }

          if(file_id !== undefined) {
            var context_url = document.location.href;
            var file_url = context_url.substring(0,context_url.lastIndexOf("/")) + "/" + file_id;
            return "<a href='" + file_url +"' target='_blank' title=" + file_id + ">Link<span style='display:none !important'>" + file_id + "</span></a>";
          } else {
            return "N/A";
          }
        }

        var result = "<table border=1><thead><tr>";

        for(var i = 0; i < columns.length; i++) {
          if(columns[i].text == "URL" || columns[i].text.trim() == "URL") {
            result += "<th>Document access</th>";
          } else {
            if(columns[i].text !== "File" && columns[i].text.trim() !== "File") {
              if(columns[i].text.charAt(0) !== "-" && columns[i].text.trim().charAt(0) !== "-") {
                result += "<th>" + columns[i].text + "</th>";
              }
            }
          }
        }

        result += "</thead><tbody>"
        for(var i = 0; i < rows.length; i++) {
          result += "<tr>";
          for(var j = 0; j < rows[i].length; j++) {
            if(columns[j].text == "URL" || columns[j].text.trim() == "URL") {
              result += "<td>" +  render_link(rows[i][j].text) + " ";
              for(var k = 0; k < rows[i].length; k++) {
                if(columns[k].text == "File" || columns[k].text.trim() == "File") {
                  result += render_file(rows[i][k].text);
                }
              }
              result += "</td>";
            } else {
              if(columns[j].text !== "File" && columns[j].text.trim() !== "File") {
                if(columns[j].text.charAt(0) !== "-" && columns[j].text.trim().charAt(0) !== "-") {
                  result += "<td>" + rows[i][j].text + "</td>";
                }
              }
            }
          }
          result += "</tr>";
        }
        result += "</tbody></table>";

        return result;
      }

      if ($.fn.DataTable.isDataTable(".table-render-preview")) {
        $('.table-render-preview').DataTable().clear().destroy();
      }

      var new_el = document.createElement("table");
      new_el.className = "table-render-preview";
      new_el.innerHTML = make_table_html(columns, rows);
      table_placeholder.parentNode.replaceChild(new_el, table_placeholder);

      var document_access_col = 100;
      var visible_columns = 0;
      for(var col = 0; col < columns.length; col++) {
        if(columns[col].text.charAt(0) !== "-" && columns[col].text.trim().charAt(0) !== "-") {
          if(columns[col].text == "URL") {
            break;
          }
          visible_columns++;
        }
      }
      document_access_col = visible_columns; // the index of URL column (without counting invisible columns)

      var the_table = $('.table-render-preview').dataTable({
        "destroy": true,
        aaSorting: [],
        "columnDefs": [
          { "orderable": false, "targets": document_access_col },
          { "searchable": false, "targets": document_access_col }
        ]
      });

      $(".dataTables_wrapper").prepend(make_filters_html(filters));

      $(".search-filter").on("click", function() {
        if($(this).hasClass("is-selected")) {
          $(this).removeClass("is-selected");
          the_table.fnFilter('');
        } else {
          var search_text = $(this).text();
          if(search_text == "Show all") {
            the_table.fnFilter('');
          } else {
            the_table.fnFilter('"' + search_text + '"');
          }
          $(".search-filter").removeClass("is-selected");
          $(this).addClass("is-selected");
        }
      });
    }
  }
}
</script>

<style scoped lang="less">
  @import "./../less/colors.less";
  @import "./../less/tablepreview.less";
</style>
