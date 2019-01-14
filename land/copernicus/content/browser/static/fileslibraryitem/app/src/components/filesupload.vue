<template>
  <div class="container">
    <label>File</label>
    <input type="file" id="file" ref="file" v-on:change="handle_file_upload()"/>
    <button v-on:click="submit_file()">Upload</button>
  </div>
</template>

<script>
export default {
  name: 'filesupload',
  methods: {
    handle_file_upload() {
      alert("Change");
    },
    submit_file() {
      alert("Upload");
    }
  }
}
</script>
