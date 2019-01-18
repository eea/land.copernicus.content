<template>
  <div class="form-container">
    <label>Files</label>
    <input type="file" id="files" ref="files" name="files" multiple v-on:change="handle_files_upload()"/>
    <button v-on:click="submit_files()">Upload</button>
    {{msg}}
  </div>
</template>

<script>
import axios from 'axios'

export default {

  name: 'filesupload',
  data(){
    return {
      files: '',
      msg: 'Select files'
    }
  },
  methods: {
    add_to_list_of_uploaded_files(file_id) {
      this.$parent.files.push(file_id);
    },

    handle_files_upload() {
      this.files = this.$refs.files.files;
    },
    submit_file() {
      let self = this;

      self.msg = "Uploading....";
      let form_data = new FormData();
      for(var i = 0; i < this.files.length; i++) {
        let file = this.files[i];

        formData.append('files[' + i + ']', file);
      }

      axios.post('./admin_files_library', form_data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(function(response){
        self.msg = "Success";
        var upload_status = response.data;
        // self.add_to_list_of_uploaded_files(file_id);
        console.log(upload_status);
      }).catch(function(){
        self.msg = "Failure";
      });
    }
  }
}
</script>
