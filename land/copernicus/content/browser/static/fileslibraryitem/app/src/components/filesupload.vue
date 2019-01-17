<template>
  <div class="form-container">
    <form class="files-upload-form" ref="files_upload_form"
          action="./admin_files_library" method="post" enctype="multipart/form-data">
        <label>File</label>
        <input type="file" id="file" ref="file" name="file" v-on:change="handle_file_upload()"/>
        <button v-on:click="submit_file()">Upload</button>
    </form>
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
      // this.$refs.files_upload_form.submit();
      let form_data = new FormData();
      form_data.append('file', this.file);

      axios.post('./admin_files_library', form_data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(function(){
        debugger;
        console.log('SUCCESS!!');
      }).catch(function(){
        console.log('FAILURE!!');
      });
    }
  }
}
</script>
