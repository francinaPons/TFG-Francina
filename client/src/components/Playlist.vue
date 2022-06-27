<template>
  <div style="margin-bottom: 100px;">
    <h1>Llistes de reproducció:</h1>
    <div id="contentView" v-if="seenContent">
      <div class="row" style="margin-bottom: 2%">
        <div class="col-3">
          Tria el mode de reproducció
          <b-form-select
          :options="options"
          style="margin-left: 1%; width: 150px"
          v-model="selected"
        ></b-form-select>
        <!--<div class="mt-3" v-if="selected === 'inter' || selected === 'rndm-inter' ">
            Fitxer intercalat:
            {{ intercalatedFile }}
          </div>-->
        </div>
      </div>
      <div class="row">
        <div class="col-2">
          <b>Llistes disponibles:</b>
          <b-form-group
          label="Filtra"
          label-for="filter-input"
          label-cols-sm="3"
          label-align-sm="right"
          label-size="sm"
          class=""
        >
          <b-input-group size="sm">
            <b-form-input
              id="filter-input"
              v-model="filter"
              type="search"
              placeholder="Escriu un tag"
            ></b-form-input>
          </b-input-group>
          </b-form-group>
          <b-table
            :striped="true"
            :bordered="true"
            :small="true"
            :hover="true"
            :items="playlists"
            :fields="fields"
            :filter="filter"
            :filter-included-fields="filterOn"
            sort-icon-left
            selectable
            select-mode='single'
            @row-selected="updatePlaylist"

          >
            <template #cell(tags)="data">

              <span v-for="tag in data.value">
                {{ tag.name }}
              </span>
            </template>
          </b-table>

          <!--<b-list-group class="list-group">
            <b-list-group-item
              v-for="item in playlists"
              v-bind:key="item.name"
              class="list-group-item"
              @click="updatePlaylist(item)"
            >
              {{ item.name }}
            </b-list-group-item>
          </b-list-group>-->
          <!--<div style="cursor: pointer" v-for="item in playlists"
               v-bind:key="item" @click="updatePlaylist(item)">
            - {{ item.name }}
          </div>-->
        </div>
        <div class="col-9">
          <div style="max-width: 90%">
              <vue-good-table
                :columns="columns"
                :pagination-options="{enabled: true, perPage: 25,
        nextLabel: 'Següent',
        prevLabel: 'Anterior',
        rowsPerPageLabel: 'elements per pàgina',
        ofLabel: 'de',
        pageLabel: 'pàgina', // for 'pages' mode
        allLabel: 'Tots',}"
                :rows="files"
                :search-options="{enabled: true}"
                :selected="enabled"
                @on-row-click="onRowClick"
                max-height="300px"
                style="color: #0032ce"
              >
                <template slot="table-row" slot-scope="props">
                  <span v-if="props.column.field === 'duration'">
                    <span
                      v-if="props.row.duration !== null"
                      >{{props.row.duration}}</span
                    >
                  </span>
                  <span v-else>
                    {{props.formattedRow[props.column.field]}}
                  </span>
                </template>
                <template slot="table-row" slot-scope="props">
                  <span v-if="props.column.field === 'priority'">
                    <span v-for="i in props.row.priority">
                      <b-icon-star-fill></b-icon-star-fill>
                    </span>
                  </span>
                </template>
              </vue-good-table>
          </div>
        </div>
        <!--<div class="col-1">
          <img src="../../static/logo_blanc.png" alt="Image">
          <b-img thumbnail fluid v-if="fileIsChoosen" v-bind:src=imageSource alt="Image" width="300" height="200"></b-img>
        </div>-->
      </div>
      <div class="row" style="display: flex; justify-content: space-around; margin-top: 2rem" >
        <!--<b-modal @hidden="resetModal" @ok="handleOk(tagsPlaylist)"
                   @show="resetModal"
                   centered
                   id="modal-center"
                   title="Guardar Playlist">
            <b-form-group
              class="my-4"
              id="fieldset-1"
              label="Com vols anomenar aquesta playlist?"
              label-for="input-1"
            >
              <b-form-input id="input-1" v-model="new_playlist_name"></b-form-input>
            </b-form-group>
            <b-form-group
              class="my-4"
              id="fieldset-2"
              label="Introdueix els tags de la playlist"
              label-for="input-2"
            >
                <vue-taggable-select
                v-model="tagsPlaylist"
                placeholder="Introdueix tags"
                :taggable="true"
                :options="tags"
                ></vue-taggable-select>
            </b-form-group>
        </b-modal>-->
        <b-button @click="removeList()" variant="danger">
          Esborrar la llista</b-button
        >
        <b-button @click="removeFile" v-if="fileIsChoosen" variant="danger">
          Esborrar fitxer de la llista</b-button
        >
        <!--<b-button @click="playNext" v-b-modal="addToPlayList-modal"
                  v-if="fileIsChoosen" variant="outline-primary">
          Reproduir després
        </b-button>-->

        <b-button @click="selected === 'inter' || selected === 'rndm-inter'
        ? $bvModal.show('modal-1'): setupPlaylist()" variant="outline-primary">
          <b-icon-play></b-icon-play>
          Reproduir llista
        </b-button>

        <b-modal id="modal-1" v-if="selected === 'inter'" title="Fitxer intercalat" @show="resetModal"
          @hidden="resetModal"
          @ok="handleOk"
          class="modal-backdrop fade in"  hide-backdrop aria-hidden="true">
          <p class="my-4">Selecciona el fitxer intercalat</p>
          <b-form-select
          :options="files"
          text-field="name"
          value-field="name"
          v-model="selectedIn"
        >
            <b-form-select-option :value="null">Fitxer "default"</b-form-select-option>
          </b-form-select>
          <!--<b-form-select v-model="selectedIn" :options="files"
            text-field="name">
            <b-form-select-option :value="null">Fitxer "default"</b-form-select-option>
          </b-form-select>-->

        </b-modal>
        <!--<b-button
          @click="setIntercalated"
          v-b-modal="addToPlayList-modal"
          v-if="fileIsChoosen && (selected === 'inter' || selected === 'rndm-inter')"
          variant="outline-primary"
        >
          Seleccionar com a fitxer intercalat
        </b-button>-->
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-alert, no-console */
import axios from 'axios';

export default {
  name: 'Playlist',

  mounted() {
    // this.getFiles();
    this.getTags();
    this.getPlaylists()
  },
  destroy() {
    clearInterval(this.timer);
  },
  data() {
    return {
      enabled: false,
      videosType: ['.mp4', '.mkv', '.m4v', '.flv', '.webm', '.ogg'],
      previousRow: '',
      timer: '',
      files: [],
      seenContent: true,
      fileIsChoosen: false,
      intercalatedFile: '',
      imageSource: null,
      urlRPI: 'http://127.0.0.1:80/content',
      selectedFileName: 0,
      duration: 0,
      columns: [
        {
          label: 'Nom',
          field: 'name',
        },
        {
          label: 'Tipus',
          field: 'type',
        },
        {
          label: 'Durada en segons (només Imatges)',
          field: 'duration',
          type: 'number',
        },
        {
          label: 'Prioritat',
          field: 'priority',
        },
      ],
      selected: 'seq',
      options: [
        { value: null, text: 'Seqüencial' },
        { value: 'inter', text: 'Intercalat' },
        { value: 'rndm', text: 'Aleatori' },
        { value: 'rndm-inter', text: 'Aleatori-Intercalat' },
      ],
      new_playlist_name: '',
      tags: [],
      playlists: [],
      selectedIn: '',
      filter: null,
      fields: ['name', 'tags'],
      filterOn: ['tags']
    };
  },
  methods: {
    previewFile(path) {
      console.log('path:');
      console.log(path);
      this.imageSource = `~/thumbnail/${path}`;
    },
    /*
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
        // eslint-disable-next-line radix
        this.setNext(fileName, parseInt(inputDuration), 'Image');
      }
    },
    setIntercalated() {
      const fileName = this.selectedFileName;
      const extension = fileName.substring(fileName.lastIndexOf('.'));
      if (this.videosType.includes(extension)) {
        this.setIntercalatedAXIOS(fileName, this.duration, 'video');
      } else {
        let inputDuration;
        inputDuration = prompt(`${fileName}\n Afegir durada en segons: `);
        if (inputDuration === null) {
          inputDuration = 0;
        }
        // eslint-disable-next-line radix
        this.setIntercalatedAXIOS(fileName, parseInt(inputDuration), 'Image');
      }
    },*/
    /*
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
          // eslint-disable-next-line no-alert
          alert(error.response.data.message);
        });
    },
    setIntercalatedAXIOS(fname, fduration, ftype) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/intercalatedEntry',
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
    resetModal() {
        this.intercalatedSelector = ''
    },
    handleOk(bvModalEvent) {
      console.log(this.playlist_name)
      console.log(this.selectedIn)
      console.log(this.files)
      if (this.selectedIn) {
        this.intercalatedFile = this.selectedIn
      }
      else {
        this.intercalatedFile = ""
      }
      this.setupPlaylist()
    },
    savePlaylist(tagsPlaylist) {
      // console.log(this.files)
      // console.log(tagsPlaylist)
      axios({
        method: 'post',
        url: 'http://127.0.0.1:80/savePlaylist',
        data: {
          name: this.new_playlist_name,
          items: this.files,
          tags: tagsPlaylist,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        alert("Afegida la playlist " + res.data.playlist.name);
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    removeFile() {
      axios({
        method: 'put',
        url: 'http://127.0.0.1:80/playlists',
        data: {
          playlist_name: this.playlist_name,
          item_name: this.selectedFileName
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        alert("Item esborrat");
        this.getPlaylists()
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
      // this.removeFileREQUEST(this.selectedFileName);
    },
    removeList() {
      console.log(this.playlist_name)
       axios({
        method: 'delete',
        url: 'http://127.0.0.1:80/playlists/' + this.playlist_name,
        data: {
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        this.getPlaylists()
        alert("Eliminada la playlist " + res.data.playlist.name);
      })
      .catch((error) => {
        alert(error.response.data.message);
      });
    },
    /*
    removeFileREQUEST(fName) {
      if (this.previousRow !== '') {
        this.previousRow.event.target.parentElement.bgColor = '';
      }
      if (this.intercalatedFile === fName) {
        this.removeIntercalatedREQUEST();
        this.intercalatedFile = 'default.mp4';
      }
      const path = `${'http://127.0.0.1:8000/playlistEntry/'}${fName}`;
      axios.delete(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          console.log(res);
          this.getFiles();
          this.fileIsChoosen = false;
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    removeIntercalatedREQUEST() {
      const path = 'http://127.0.0.1:8000/intercalatedEntry';
      axios.delete(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          console.log(res);
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },*/
    onRowClick(params) {
      this.imageSource = `/thumbnail/${params.row.name}`;
      this.selectedFileName = params.row.name;
      this.fileIsChoosen = true;
      // eslint-disable-next-line no-param-reassign
      params.event.target.parentElement.bgColor = '#f1f5fd';
      if (this.previousRow === '') {
        this.previousRow = params;
      } else {
        this.previousRow.event.target.parentElement.bgColor = '';
        this.previousRow = params;
      }
    },
    /*
    getFiles() {
      if (Object.keys(this.$route.query.token).length !== 0) {
        const path = 'http://127.0.0.1:80/playlist';
        axios.get(path, { auth: { username: this.$route.query.token } })
          .then((res) => {
            this.files = res.data.Playlist;
          })
          .catch((error) => {
            console.log(error.response.data.message);
            if (error.response.data.message === 'La sessió ha caducat, inicia sessió de nou') {
              alert('La sessió ha caducat. Introdueix les teves credencials un altre cop');
              this.$router.replace({ path: '/' });
              this.$root.$emit('login', false);
              clearInterval(this.timer);
            }
          });
      }
    },*/
    getTags() {
      const path = 'http://127.0.0.1:80/tags';
      axios.get(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          console.log(res.data.tags);
          for (let i = 0; i < res.data.tags.length; i += 1) {
            console.log(res.data.tags[i]);
            this.tags.push(res.data.tags[i].name);
          }
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
    /*
    getMode() {
      // this.selectedFileName = ''
      // this.fileIsChoosen = false
      const path = 'http://127.0.0.1:8000/mode';
      axios.get(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          const mode = res.data.message;
          if (mode === 'seq') {
            this.selected = null;
          } else {
            this.selected = mode;
          }
          // this.changeTable()
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
    changeMode() {
      let m = this.selected;
      if (this.selected === null) {
        m = 'seq';
      }
      axios({
        method: 'put',
        url: 'http://127.0.0.1:8000/mode',
        data: {
          mode: m,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        console(res.data.message);
        // this.changeTable()
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    changeTable() {
      if (this.selected === 'rndm') {
        this.columns = [
          {
            label: 'Nom',
            field: 'name',
          },
          {
            label: 'Tipus',
            field: 'type',
          },
          {
            label: 'Durada en segons (només Imatges)',
            field: 'duration',
            type: 'number',
          },
          {
            label: 'Reproduït',
            field: 'played',
          },
        ];
      } else {
        this.columns = [
          {
            label: 'Nom',
            field: 'name',
          },
          {
            label: 'Tipus',
            field: 'type',
          },
          {
            label: 'Durada en segons (només Imatges)',
            field: 'duration',
            type: 'number',
          },
        ];
      }
    },

    getIntercalatedFile() {
      // this.selectedFileName = ''
      // this.fileIsChoosen = false
      const path = 'http://127.0.0.1:8000/intercalatedEntry';
      axios.get(path)
        .then((res) => {
          this.intercalatedFile = res.data.metadata.path;
          this.intercalatedFile = this.intercalatedFile.substring(this.intercalatedFile.lastIndexOf('/'));
          this.intercalatedFile = this.intercalatedFile.substring(1);
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
    methodUpload() {
      this.seenContent = !this.seenContent;
      // this.getFiles();
    },*/
    updatePlaylist(playlist) {
      console.log(playlist[0])
      playlist = playlist[0]
      this.files = playlist.items
      this.playlist_name = playlist.name
      this.fileIsChoosen = false
      // const obj = arr.find(({ data }) => data === name);
      // console.log(obj);
      /* for (let i = 0; i < this.playlists.length; i += 1) {
        if (this.playlists[i].name === playlist.name) {
          console.log(this.playlists[i]);
        }
      } */
    },
    getPlaylists() {
      this.playlists = []
      if (Object.keys(this.$route.query.token).length !== 0) {
        axios({
          method: 'get',
          url: 'http://127.0.0.1:80/playlistslist',
          auth: {username: this.$route.query.token},
        }).then((res) => {
          for (let i = 0; i < res.data.playlists.length; i += 1) {
            console.log(res.data.playlists[i]);
            this.playlists.push(res.data.playlists[i]);
          }
          if (this.playlists.length > 0) {
            // console.log(this.playlists[0].items)
            this.files = this.playlists[0].items
            this.playlist_name = this.playlists[0].name
          }
          console.log(res.data.playlists);
        })
          .catch((error) => {
            alert(error.response.data.message);
            if (error.response.data.message === 'La sessió ha caducat, inicia sessió de nou') {
              alert('La sessió ha caducat. Introdueix les teves credencials un altre cop');
              this.$router.replace({path: '/'});
              this.$root.$emit('login', false);
              clearInterval(this.timer);
            }
          });
      }
    },
    setupPlaylist() {
      let mode = 'seq'
      if (this.selected != null) {
        mode = this.selected
      }
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/setPlaylist',
        data: {
          inter: this.intercalatedFile,
          name: this.playlist_name,
          items: this.files,
          mode: mode,
          status: this.status
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        alert(res.data.message);
      })
        .catch((error) => {
          // eslint-disable-next-line no-alert
          alert(error.response.data.message);
        });
      console.log("sending playlist to billboard")

    }
  },

};
/* eslint-enable no-alert, no-console */
</script>
<style scoped>
.list-group {
  max-height: 75%;
  overflow: scroll;
  -webkit-overflow-scrolling: touch;
  cursor: pointer;
}
</style>
