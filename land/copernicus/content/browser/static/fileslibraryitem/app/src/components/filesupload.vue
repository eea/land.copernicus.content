<template>
  <div class="files-upload-container">
    <div class="controls">
      <label>Files</label>
      <input type="file" id="files" ref="files" name="files" multiple v-on:change="handle_files_upload()"/>
      <button v-on:click="submit_files()">Upload</button>
    </div>
    <div class="status">
      <label>Status:</label>
      {{msg}}
    </div>
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
    submit_files() {
      let self = this;

      self.msg = "Uploading....";
      let form_data = new FormData();
      for(var i = 0; i < this.files.length; i++) {
        let file = this.files[i];

        form_data.append('files[' + i + ']', file);
      }

      axios.post('./admin_files_library', form_data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(function(response){
        self.msg = "Success: ";
        var files_status = response.data;
        for(var i = 0; i < files_status.length; i++) {
          if(files_status[i].status == "success") {
            self.add_to_list_of_uploaded_files(files_status[i].filename);
            self.msg += files_status[i].filename + " ";
          }
        }
      }).catch(function(){
        self.msg = "Failure";
      });
    }
  }
}
</script>

<style scoped lang="less">
  @import "./../less/colors.less";
  @import "./../less/filesupload.less";
</style>
