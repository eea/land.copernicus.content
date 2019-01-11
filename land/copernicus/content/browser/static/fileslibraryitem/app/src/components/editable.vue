<template>
  <div contenteditable="true" @blur="emitChange">
    {{ content }}
  </div>
</template>

<script>
export default {
  name: 'editable',
  props: ['content'],
  methods: {
    emitChange(ev) {
      this.$emit('update', ev.target.textContent)
    }
  }
}
</script>

<style scoped>
</style>
