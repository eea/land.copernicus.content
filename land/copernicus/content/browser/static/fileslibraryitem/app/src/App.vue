<template>
  <div id="datatables-admin">
    <h1>Datatables admin</h1>

    <table id="editor">
      <thead>
        <tr>
          <th v-for="(column, index_col) in columns" :key="column.id">
            <i class="fas fa-long-arrow-alt-left fa-2x dta-btn move-col-left" title="Move column to left" v-on:click="move_col_to_left(index_col)"></i>
            <i class="fas fa-long-arrow-alt-right fa-2x dta-btn move-col-right" title="Move column to right" v-on:click="move_col_to_right(index_col)"></i>
            <i class="fas fa-plus fa-2x dta-btn add-col" title="Add a column after this one" v-on:click="add_col(index_col + 1)"></i>
            <i class="fas fa-times fa-2x dta-btn delete-col" title="Delete this column" v-on:click="delete_col(index_col)"></i>
            <br />
            <editable :content="columns[index_col].text" v-on:update="update_col($event, index_col)"></editable>
          </th>
          <th>
            <i class="fas fa-plus fa-2x dta-btn add-col" title="Add a column" v-on:click="add_col(0)"></i>
            <i class="fas fa-plus fa-2x dta-btn add-row" title="Add a row" v-on:click="add_row(0)"></i>
            <i class="fas fa-times fa-2x dta-btn delete-all-cols" title="Delete all columns" v-on:click="delete_all_cols"></i>
            <i class="fas fa-times fa-2x dta-btn delete-all-rows" title="Delete all rows" v-on:click="delete_all_rows"></i>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index_row) in rows" :key="index_row">
          <td v-for="(column, index_col) in columns" :key="column.id">
            <editable :content="rows[index_row][index_col].text" v-on:update="update_row($event, index_row, index_col)"></editable>
          <td>
            <i class="fas fa-long-arrow-alt-up fa-2x dta-btn move-row-up" v-on:click="move_row_up(index_row)" title="Move row up"></i>
            <i class="fas fa-long-arrow-alt-down fa-2x dta-btn move-row-down" v-on:click="move_row_down(index_row)" title="Move row down"></i>
            <i class="fas fa-plus fa-2x dta-btn add-row" title="Add a row under this one" v-on:click="add_row(index_row + 1)"></i>
            <i class="fas fa-times fa-2x dta-btn delete-row" title="Delete this row" v-on:click="delete_row(index_row)"></i>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="IS_DEBUG_MODE">
      <p>
        <b>Columns:</b>
        <span v-text="columns"></span>
      </p>
      <p>
        <b>Rows:</b>
        <span v-text="rows"></span>
      </p>
    </div>

    <table-preview></table-preview>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      LOREM: "Click me to edit",
      NONE: "",
      IS_DEBUG_MODE: false,  // Show or hide data
      filters: [
        {
          'id': 'filter01',
          'text': 'Demo category'
        },
        {
          'id': 'filter02',
          'text': 'Demo category 2'
        },
        {
          'id': 'filter02',
          'text': 'Sub-category 3'
        }
      ],
      columns: [
        {
          'id': '001',
          'text': 'Click me to edit'
        },
        {
          'id': '002',
          'text': 'Demo column 2'
        },
        {
          'id': '003',
          'text': 'Demo column 3'
        },
        {
          'id': '004',
          'text': 'URL'
        }
      ],
      rows: [
        [
          {
            'id': '005',
            'text': 'Demo category'
          },
          {
            'id': '006',
            'text': 'Sub-category 1'
          },
          {
            'id': '007',
            'text': 'col3 data1'
          },
          {
            'id': '008',
            'text': 'https://www.google.com'
          }
        ],

        [
          {
            'id': '009',
            'text': 'Demo category'
          },
          {
            'id': '010',
            'text': 'Sub-category 2'
          },
          {
            'id': '011',
            'text': 'col3 data2'
          },
          {
            'id': '012',
            'text': 'https://www.yahoo.com'
          }
        ],

        [
          {
            'id': '013',
            'text': 'Demo category 2'
          },
          {
            'id': '014',
            'text': 'Sub-category 3'
          },
          {
            'id': '015',
            'text': 'col3 data3'
          },
          {
            'id': '016',
            'text': 'https://www.yahoo.com'
          }
        ]
      ]
    }
  },
  methods: {
    generate_random(min, max) {
        return Math.random() * (max - min) + min;
    },

    generate_id: function() {
      return '__key_prefix__' + Date.now() + '_' + this.generate_random(10000, 99999);
    },

    new_data: function(text) {
      return {
        'id': this.generate_id(),
        'text': text
      }
    },

    refresh: function() {
      for(var i = 0; i < this.columns.length; i++) {
        this.columns[i].id = this.generate_id();
      }

      for(var i = 0; i < this.rows.length; i++) {
        for(var j = 0; j < this.columns.length; j++) {
          this.rows[i][j].id = this.generate_id();
        }
      }

      this.$forceUpdate();
    },

    update_col: function(content, col_index) {
      this.columns[col_index].text = content.trim();
      this.refresh();
    },

    update_row: function(content, row_index, col_index) {
      this.rows[row_index][col_index].text = content.trim();
      this.refresh();
    },

    add_col: function(col_index) {
      // Add a new column at given index
      this.columns.splice(col_index, 0, this.new_data(this.LOREM));
      for(var i = 0; i < this.rows.length; i++) {
        var row = this.rows[i];
        row.splice(col_index, 0, this.new_data(this.NONE));
      }
      this.refresh();
    },

    delete_col: function(col_index, skip_confirm = false) {
      if(!skip_confirm) {
        var result = confirm("Are you sure you want to delete this column?");
        if(!result) {
          return;
        }
      }

      // Remove column
      this.columns.splice(col_index, 1);

      // Remove related items in rows
      for(var i = 0; i < this.rows.length; i++) {
        var row = this.rows[i];
        row.splice(col_index, 1);
      }

      this.refresh();
    },

    add_row: function(row_index) {
      // Add a new row at given index
      this.rows.splice(row_index, 0, new Array(this.columns.length));

      for(var i = 0; i < this.columns.length; i++) {
        this.rows[row_index][i] = this.new_data(this.NONE);
      }

      this.refresh();
    },

    delete_row: function(row_index, skip_confirm = false) {
      if(!skip_confirm) {
        var result = confirm("Are you sure you want to delete this row?");
        if(!result) {
          return;
        }
      }

      this.rows.splice(row_index, 1);

      this.refresh();
    },

    delete_all_rows: function() {
      var result = confirm("Are you sure you want to delete all rows?");
      if(!result) {
        return;
      }

      var nr_rows = this.rows.length;
      for(var i = 0; i < nr_rows; i++) {
        this.delete_row(0, true);
      }

      this.refresh();
    },

    delete_all_cols: function() {
      var result = confirm("Are you sure you want to delete all columns?");
      if(!result) {
        return;
      }

      var nr_cols = this.columns.length;
      for(var i = 0; i < nr_cols; i++) {
        this.delete_col(0, true);
      }

      this.refresh();
    },

    move_col_to_left: function(col_index) {
      if(col_index == 0) {
        return;
      }
      var temp = this.columns[col_index - 1].text;
      this.columns[col_index - 1].text = this.columns[col_index].text;
      this.columns[col_index].text = temp;

      for(var i = 0; i < this.rows.length; i++) {
        temp = this.rows[i][col_index - 1].text;
        this.rows[i][col_index - 1].text = this.rows[i][col_index].text;
        this.rows[i][col_index].text = temp;
      }

      this.columns = this.columns.slice();
      this.rows = this.rows.slice();
      this.refresh();
    },

    move_col_to_right: function(col_index) {
      if(col_index == this.columns.length - 1) {
        return;
      }
      var temp = this.columns[col_index + 1].text;
      this.columns[col_index + 1].text = this.columns[col_index].text;
      this.columns[col_index].text = temp;

      for(var i = 0; i < this.rows.length; i++) {
        temp = this.rows[i][col_index + 1].text;
        this.rows[i][col_index + 1].text = this.rows[i][col_index].text;
        this.rows[i][col_index].text = temp;
      }

      this.columns = this.columns.slice();
      this.rows = this.rows.slice();
      this.refresh();
    },

    move_row_up: function(row_index) {
      if(row_index == 0) {
        return;
      }
      var temp = this.rows[row_index - 1];
      this.rows[row_index - 1] = this.rows[row_index];
      this.rows[row_index] = temp;

      this.columns = this.columns.slice();
      this.rows = this.rows.slice();
      this.refresh();
    },

    move_row_down: function(row_index) {
      if(row_index == this.rows.length - 1) {
        return;
      }
      var temp = this.rows[row_index + 1];
      this.rows[row_index + 1] = this.rows[row_index];
      this.rows[row_index] = temp;

      this.columns = this.columns.slice();
      this.rows = this.rows.slice();
      this.refresh();
    }
  }
}
</script>

<style>@import url("styles.css");</style>
