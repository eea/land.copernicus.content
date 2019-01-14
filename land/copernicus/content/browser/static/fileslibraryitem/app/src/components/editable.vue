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
  div.editable-div {
    background: #FFFFFF;
    color: #000000;
    padding: 6px;
    border-bottom: 3px solid #FFFFFF;

    &:hover {
      background: #EEEEEE;
      border-bottom: 3px solid #FFFFFF;
    }

    &:focus {
      background: #EEEEEE;
      outline: none;
      border-bottom: 3px solid #CCCCCC;
    }
  }

</style>
