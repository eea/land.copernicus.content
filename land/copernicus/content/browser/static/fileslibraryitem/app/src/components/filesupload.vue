<template>
  <div class="form-container">
    <label>File</label>
    <input type="file" id="file" ref="file" name="file" v-on:change="handle_file_upload()"/>
    <button v-on:click="submit_file()">Upload</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {

  name: 'filesupload',
  data(){
    return {
      file: ''
    }
  },
  methods: {
    handle_file_upload() {
      this.file = this.$refs.file.files[0];
    },
    submit_file() {
      let form_data = new FormData();
      form_data.append('file', this.file);

      axios.post('./admin_files_library', form_data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(function(){
        console.log('SUCCESS!!');
      }).catch(function(){
        console.log('FAILURE!!');
      });
    }
  }
}
</script>
