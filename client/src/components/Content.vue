<template>
<div style="margin-bottom: 100px;">
  <div v-if="seenContent && contentSettings" id="contentView">
    <div style="display: flex">
      <div style="width: 90%; margin: auto;">
        <vue-good-table ref ='my-table' style="color: #0032ce;"
                        :selected="enabled" :columns="columns" :rows="files"
                        max-height="300px" :search-options="{enabled: true}"
                        :pagination-options="{enabled: true, perPage: 25,
                        nextLabel: 'Següent',
                        prevLabel: 'Anterior',
                        rowsPerPageLabel: 'elements per pàgina',
                        ofLabel: 'de',
                        pageLabel: 'pàgina', // for 'pages' mode
                        allLabel: 'Tots',}" @on-row-click="onRowClick"
                        @on-selected-rows-change="selectionChanged"
                        :select-options="{
                        enabled: true,
                        selectOnCheckboxOnly: false, // only select when checkbox is clicked instead of the row
                        selectionInfoClass: 'custom-class',
                        selectionText: 'Elements seleccionats',
                               clearSelectionText: 'clear',
                        disableSelectInfo: true, // disable the select info panel on top
                        selectAllByGroup: true, // when used in combination with a grouped table, add a checkbox in the header row to check/uncheck the entire group
                        }">
        <template slot="table-row" slot-scope="props">
          <span v-if="props.column.field === 'size'">
          <span >{{props.row.size/1000000}}</span>
          </span>
          <span v-else>
            {{ props.formattedRow[props.column.field] }}
          </span>
        </template>
        </vue-good-table>
        <div style="margin-top: 2rem; display: flex; align-content: center; justify-content: space-around">
          <b-button variant="outline-primary" @click="methodUpload">Afegir Contingut</b-button>
        <b-button v-if="filesAreChoosen" variant="danger" @click="removeFile">Esborrar els fitxers seleccionats</b-button>
        <b-button variant="outline-primary"v-if="filesAreChoosen" @click="addToPlaylist2()">Afegir a una llista de reproducció</b-button>

        </div>
        </div>
      <div>
        <span style="display:inline-block; width:50px;"></span>
        <b-img thumbnail fluid v-if="fileIsChoosen" :src="imageSource" alt="Image" width="300" height="200"></b-img>
      </div>
    </div>
  </div>
  <div v-if="!seenContent" id="contentUploadView" style="width:800px; margin:0 auto;">
    <ContentUpload></ContentUpload>

    <b-button variant="outline-primary" @click="methodUpload">Enrere</b-button>
  </div>
  <div v-if="!contentSettings">
    <ContentSettings :files="multipleRows"></ContentSettings>
    <b-button variant="outline-primary" @click="methodUploadContentSettings">Enrere</b-button>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import ContentUpload from './ContentUpload.vue';
import ContentSettings from './ContentSettings.vue';

export default {
  name: 'Content',
  components: {
    ContentUpload,
    ContentSettings
  },
  /*
      Defines the data used by the component
    */
  created() {
    this.getFiles();
  },
  data() {
    return {
      videosType: ['.mp4', '.mkv', '.m4v', '.flv', '.webm', '.ogg'],
      multipleRows: [],
      previousRow: '',
      files: [],
      enabled: true,
      seenContent: true,
      fileIsChoosen: false,
      filesAreChoosen: false,
      imageSource: null,
      urlRPI: 'http://127.0.0.1:80/content',
      selectedFileID: 0,
      selectedFileName: 0,
      fileToSend: 0,
      duration: '',
      contentSettings: true,
      columns: [
        {
          label: 'Nom',
          field: 'name',
        },
        {
          label: 'Mida (en MB)',
          field: 'size',
          type: 'decimal',
        },
      ],
    };
  },
  methods: {
    previewFile(path) {
      console.log('path:');
      console.log(path);
      path = path.split('.')
      this.imageSource = `/thumbnails/${path[0]}`;
      console.log(this.imageSource);
      // document.getElementById('preview').alt = path
      // this.$root.$emit('bv::show::modal', 'preview-modal', '#btnShow')
    },
    addToPlaylist2() {
      console.log(this.files)
      this.contentSettings = !this.contentSettings;

    },
    addToPlaylist() {
      let fileName;
      let extension;
      if (this.multipleRows.length !== 0) {
        let i = 0;
        for (i; i < this.multipleRows.length; i++) {
          var inputDurationM;
          // this.$root.$emit('bv::show::modal', 'addToPlayList-modal')
          fileName = this.multipleRows[i].name;
          extension = fileName.substring(fileName.lastIndexOf('.'));
          if (this.videosType.includes(extension)) { // if (!(extension in this.videosType)) {
            this.addToPlaylistPOST(fileName, 0, 'video');
          } else {
            inputDurationM = prompt(`${fileName}\n Afegir durada en segons:`);
            if (inputDurationM === null) {
              inputDurationM = 0;
            }
            this.addToPlaylistPOST(fileName, parseInt(inputDurationM), 'Image');
          }
        }
      } else {
        fileName = this.selectedFileName;
        extension = fileName.substring(fileName.lastIndexOf('.'));
        if (this.videosType.includes(extension)) {
          this.addToPlaylistPOST(fileName, this.duration, 'video');
        } else {
          let inputDuration;
          inputDuration = prompt(`${fileName}\n Afegir durada en segons: `);
          if (inputDuration === null) {
            inputDuration = 0;
          }
          this.addToPlaylistPOST(fileName, parseInt(inputDuration), 'Image');
        }
      }
    },
    playNext() {
      const fileName = this.selectedFileName;
      const extension = fileName.substring(fileName.lastIndexOf('.'));
      if (this.videosType.includes(extension)) {
        this.setNext(fileName, this.duration, 'video');
      } else {
        let inputDuration;
        inputDuration = prompt(`${fileName}\n Afegir durada en segons: `);
        if (inputDuration === null) {
          inputDuration = 0;
        }
        this.setNext(fileName, parseInt(inputDuration), 'Image');
      }
    },
    /*
    addToPlaylistPOST(fname, fduration, ftype) {
      // Save in playlist Controller
      axios({
        method: 'post',
        url: 'http://127.0.0.1:80/item',
        data: {
          name: fname,
          playlist_name: "playlist1",
          duration: fduration,
          priority: 1,
          type: ftype,
          played: 1
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        alert(res.data.message);
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
      // Save in playlist Billboard
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/playlistEntry',
        data: {
          name: fname,
          duration: fduration * 1000,
          type: ftype,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        console.log(res);
      })
        .catch((error) => {
          alert(error.response.data);
        });
    },
    setNext(fname, fduration, ftype) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/nextEntry',
        data: {
          name: fname,
          duration: fduration * 1000,
          type: ftype,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        alert(res.data.message);
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },*/
    removeFile() {
      if (this.multipleRows.length !== 0) {
        let i = 0;
        for (i; i < this.multipleRows.length; i++) {
          console.log('console.log(this.multipleRows[i].id:):');
          console.log(this.multipleRows[i].id);
          this.removeFileAXIOS(this.multipleRows[i].id);
        }
      } else {
        this.removeFileAXIOS(this.selectedFileID);
      }
      setTimeout(() => this.getFiles(), 2000);
    },
    removeFileAXIOS(fID) {
      // var id = key + 1
      console.log('fID:');
      console.log(fID);
      if (this.previousRow !== '') {
        this.previousRow.event.target.parentElement.bgColor = '';
      }
      const path = `${this.urlRPI}/${fID}`;
      axios.delete(path, {
        auth: { username: this.$route.query.token },
      }).then((res) => {
        console.log(res);
        // this.getFiles()
        this.fileIsChoosen = false;
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    onRowClick(params) {
      console.log('path:');
      const path = params.row.name;
      console.log(path);
      this.imageSource = `thumbnails/${path.split('.')[0] + '.png'}`;
      console.log(this.imageSource);
      this.selectedFileName = params.row.name;
      this.selectedFileID = params.row.id;
      this.fileIsChoosen = true;
      params.event.target.parentElement.bgColor = '#f1f5fd';
      if (this.previousRow === '') {
        this.previousRow = params;
      } else {
        this.previousRow.event.target.parentElement.bgColor = '';
        this.previousRow = params;
      }
    },
    selectionChanged(params) {
      this.multipleRows = params.selectedRows;
      console.log('selectionChanged');
      console.log(params.selectedRows);
      this.filesAreChoosen = params.selectedRows.length !== 0;
      // console.log(params.selectedRows[0].name)
    },
    getFiles() {
      this.selectedFileID = 0;
      this.selectedFileName = '';
      this.fileIsChoosen = false;
      const path = this.urlRPI;
      axios.get(path, {
        auth: { username: this.$route.query.token },
      }).then((res) => {
        this.files = res.data.content;
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    methodUpload() {
      this.seenContent = !this.seenContent;
      this.getFiles();
    },
    methodUploadContentSettings() {
      this.contentSettings = !this.contentSettings;
      this.getFiles();
    },
  },
};
</script>
