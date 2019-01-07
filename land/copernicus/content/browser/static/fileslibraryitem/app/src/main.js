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

Vue.component('table-preview', {
  template: `
    <div class="table-preview-container">
      <button class='render-table' v-on:click="render_table">Preview table</button>
      <table class="table-render-preview"></table>
    </div>
  `,
  props: ['content'],
  methods: {
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
              result += "<td>" + rows[i][j].text + "</td>";
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
