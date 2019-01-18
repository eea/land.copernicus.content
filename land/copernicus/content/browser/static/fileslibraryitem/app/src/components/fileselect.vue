<template>
  <select class="land-fileselect" @change="update_selected_file()">
    <option></option>
    <option v-for="option in this.$parent.files.slice().reverse()">{{option}}</option>
  </select>
</template>

<script>
export default {
  name: 'fileselect',
  props: ['content', 'index_row', 'index_col'],
  methods: {
    update_selected_file(ev) {
      var selected_filename = this.$el.value;
      this.$parent.update_row(selected_filename, this.index_row, this.index_col);
    }
  }
}
</script>

<style scoped lang="less">
  @import "./../less/colors.less";
  @import "./../less/fileselect.less";
</style>
