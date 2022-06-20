<template>
  <div>
    <p>Insereix les prioritats i duracions que vulguis</p>
    <b-editable-table
      bordered
      class="editable-table"
      v-model="files"
      :fields="fields"
    >
    </b-editable-table>
    <p>A quina llista vols afegir aquests items?</p>
     <b-form-select v-model="selectedPlaylist" :options="playlists" @change="getTagsPlaylist(selectedPlaylist)">
       <b-form-select-option :value="null">Selecciona una llista</b-form-select-option>
       <b-form-select-option :value="-1">Crear nova llista</b-form-select-option>
     </b-form-select>

    <div v-if="selectedPlaylist === -1">
      <b-form-group label-cols="4" label-cols-lg="2" label="Nom de la nova llista: " label-for="input">
        <b-form-input id="input" v-model="newPlaylist"></b-form-input>
      </b-form-group>
    </div>
    La playlist conté els següents tags: {{ currentTags }}
    <b-form-group v-if="selectedPlaylist !== null"
              class="my-4"
              id="fieldset-2"
              label="Introdueix els tags de la playlist"
              label-for="input-2"
            >
                <vue-taggable-select
                v-model="tagsPlaylist"
                placeholder="Introdueix tags"
                :taggable="true"
                :options="allTags"
                ></vue-taggable-select>
            </b-form-group>
    <b-button style="margin: 3%" @click="savePlaylist()">Guardar llista de reproducció</b-button>
  </div>
</template>

<script>
import BEditableTable from "bootstrap-vue-editable-table";
import { BSpinner } from "bootstrap-vue";
import axios from "axios";
export default {
  components: {
    BEditableTable,
    BSpinner,
  },
  props: ['files'],
  mounted() {
    this.getPlaylists()
    this.getTags()
  },
  data() {
    return {
      fields: [
        { id: 1, key: "name", label: "Name", type: "text", editable: false },
        { id: 2, key: "path", label: "Path", type: "text", editable: false },
        { id: 3, key: "size", label: "Mida", editable: false },
        { id: 4, key: "priority", label: "Prioritat", type: "range", min: "1",
          max: "5", editable: true },
        { id: 5, key: "duration", label: "Duració", type: "number", editable: true },
      ],
      playlists: [],
      selectedPlaylist: null,
      newPlaylist: '',
      tagsPlaylist: [],
      tags: [],
      currentTags: [],
      allTags: []
    };
  },
  methods: {
    savePlaylist() {
      console.log(this.selectedPlaylist)
      if (this.selectedPlaylist !== null && this.selectedPlaylist !== -1){
        this.newPlaylist = this.selectedPlaylist
      }
      console.log(this.files)
      console.log(this.newPlaylist)
      axios({
        method: 'post',
        url: 'http://127.0.0.1:80/savePlaylist',
        data: {
          name: this.newPlaylist,
          items: this.files,
          tags: this.tagsPlaylist,
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
          alert("Afegida la playlist " + res.data.playlist.name);
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    getPlaylists() {
      if (Object.keys(this.$route.query.token).length !== 0) {
        axios({
          method: 'get',
          url: 'http://127.0.0.1:80/playlistslist',
          auth: {username: this.$route.query.token},
        }).then((res) => {
          for (let i = 0; i < res.data.playlists.length; i += 1) {
            console.log(res.data.playlists[i]);
            this.playlists.push(res.data.playlists[i].name);
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
    getTags() {
      const path = 'http://127.0.0.1:80/tags';
      axios.get(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          console.log(res.data.tags);
          for (let i = 0; i < res.data.tags.length; i += 1) {
            console.log(res.data.tags[i]);
            this.allTags.push(res.data.tags[i].name);
          }
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },
    getTagsPlaylist(playlistName) {
      console.log(playlistName)
      this.currentTags = []
      if (playlistName !== null && playlistName !== -1) {
        const path = 'http://127.0.0.1:80/playlists/' + playlistName;
        axios.get(path, {auth: {username: this.$route.query.token}})
          .then((res) => {
            console.log(res.data.playlist.tags);
            for (var key in res.data.playlist.tags) {
              console.log(key)
              var obj = res.data.playlist.tags[key];
              console.log(obj)
              this.currentTags.push(obj.name)
            }

            // console.log(this.currentTags)
          })
          .catch((error) => {
            console.log(error.response.data.message);
          });
      }
    }
  }
};
</script>

<style>
table.editable-table {
  margin: auto;
}

table.editable-table td {
  vertical-align: middle;
}

.editable-table .data-cell {
  padding: 8px;
  vertical-align: middle;
}

</style>
