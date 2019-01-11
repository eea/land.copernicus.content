<template>
  <select @change="onChange()">
    <option></option>
    <option v-for="option in this.$parent.files">{{option}}</option>
  </select>
</template>

<script>
export default {
  name: 'fileselect',
  props: ['content', 'index_row', 'index_col'],
  methods: {
    onChange(ev) {
      var selected_filename = this.$el.value;
      this.$parent.update_row(selected_filename, this.index_row, this.index_col);
    }
  }
}
</script>

<style scoped>
</style>
