// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false

Vue.component('editable', {
  template: `
    <div contenteditable="true" @blur="emitChange">
      {{ content }}
    </div>
  `,
  props: ['content'],
  methods: {
    emitChange(ev) {
      this.$emit('update', ev.target.textContent)
    }
  }
});

Vue.component('fileselect', {
  template: `
    <select @change="onChange()">
      <option></option>
      <option v-for="option in this.$parent.files">{{option}}</option>
    </select>
  `,
  props: ['content', 'index_row', 'index_col'],
  methods: {
    onChange(ev) {
      var selected_filename = this.$el.value;
      this.$parent.update_row(selected_filename, this.index_row, this.index_col);
    }
  }
});

Vue.component('table-preview', {
  template: `
    <div class="table-preview-container">
      <button name="save-work" class='large-btn' v-on:click="save_work">Save</button>
      <button name="render-table" class='large-btn' v-on:click="render_table">Preview table</button>
      <button name="upload-files" class='large-btn' v-on:click="upload_files">Upload files</button>
      <button name="cancel-work" class='large-btn' title="The unsaved work will be lost." v-on:click="cancel_work">Cancel</button>
      <table class="table-render-preview"></table>
    </div>
  `,
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

    upload_files() {
      // TODO when new files are uploaded, the new filesnames will be available to be selected
      this.$parent.files.push("newuploadedfile1", "newuploadedfile2", "newuploadedfile3");
    },

    render_table() {
      var columns = this.$parent.columns;
      var rows = this.$parent.rows;
      var filters = this.$parent.filters;
      var table_placeholder = document.querySelector('.table-render-preview');

      function make_filters_html(filters) {
        var filters_html = "<div class='filters-container'><p><b>Search filters:</b></p><ul class='filters-list'>";
        for(var i = 0; i < filters.length; i++) {
          filters_html += "<li class='search-filter'>" + filters[i].text + "</li>";
        }
        filters_html += "</ul></div>"

        return filters_html;
      }

      function make_table_html(columns, rows) {
        function render_link(url) {
          if(url !== undefined) {
            return "<a href='" + url +"' target='_blank' title=" + url + ">Link<span style='display:none !important'>" + url + "</span></a>";
          } else {
            return "N/A";
          }
        }

        function render_file(file_id) {
          if(file_id !== undefined) {
            return "<a href='" + file_id +"' target='_blank' title=" + file_id + ">File<span style='display:none !important'>" + file_id + "</span></a>";
          } else {
            return "N/A";
          }
        }

        var result = "<table border=1><thead><tr>";

        for(var i = 0; i < columns.length; i++) {
          result += "<th>" + columns[i].text + "</th>";
        }

        result += "</thead><tbody>"
        for(var i = 0; i < rows.length; i++) {
          result += "<tr>";
          for(var j = 0; j < rows[i].length; j++) {
            if(columns[j].text == "URL" || columns[j].text.trim() == "URL") {
              result += "<td>" +  render_link(rows[i][j].text) + "</td>";
            } else {
              if(columns[j].text == "File" || columns[j].text.trim() == "File") {
                result += "<td>" +  render_file(rows[i][j].text) + "</td>";
              } else {
                result += "<td>" + rows[i][j].text + "</td>";
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

      var the_table = $('.table-render-preview').dataTable({
        "destroy": true,
        aaSorting: []
      });

      $(".dataTables_wrapper").append(make_filters_html(filters));

      $(".search-filter").on("click", function() {
        the_table.fnFilter('"' + $(this).text() + '"');
        $(".search-filter").removeClass("is-selected");
        $(this).addClass("is-selected");
      });
    }
  }
});

/* eslint-disable no-new */
new Vue({
  el: '#datatables-admin',
  template: '<App/>',
  components: { App }
});
