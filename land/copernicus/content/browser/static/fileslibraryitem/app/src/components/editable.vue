<template>
  <div contenteditable="true" @blur="emit_change" class="editable-div">{{content}}</div>
</template>

<script>
export default {
  name: 'editable',
  props: ['content'],
  methods: {
    emit_change(ev) {
      this.$emit('update', ev.target.textContent)
    }
  }
}
</script>

<style scoped lang="less">
  @import "./../less/colors.less";
  @import "./../less/editable.less";
</style>
