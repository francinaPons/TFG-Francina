<template>
<div >
    <div>
      <h1>Mode manteniment:</h1>
      <div style="max-width: 60%; margin: auto auto 2rem;">
        <h6>
          Té per objectiu treballar amb el sistema aturant la llista de reproducció.
          En activar-lo, el televisor reprodueix el fitxer default.mp4 reiteradament.
          És una manera de controlar en tot moment la reproducció, sobretot quan estem fent canvis.
          <br>
          <i>Nota: No s'activa fins que acaba de reproduir-se el contingut que es
            reproduïa en el moment d'activar-lo.</i>
        </h6>
      </div>
      <b-button  v-if="activated" variant="outline-primary" @click="switchStatus">Desactivar</b-button>
      <b-button  v-if="!activated" variant="danger" @click="switchStatus">Activar</b-button>
    </div>
    <br>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SwitchStatus',
  /*
      Defines the data used by the component
    */
  created() {
    this.getStatus();
  },
  methods: {
    switchStatus() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/status',
        data: {
        },
        auth: { username: this.$route.query.token },
      }).then((res) => {
        this.activated = !this.activated;
      })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
   /* getStatus() {
      // this.selectedFileName = ''
      // this.fileIsChoosen = false
      const path = 'http://127.0.0.1:8000/status';
      axios.get(path, { auth: { username: this.$route.query.token } })
        .then((res) => {
          const mode = res.data.message;
          if (mode === 'stop') {
            this.activated = true;
          } else {
            this.selected = false;
          }
        })
        .catch((error) => {
          console.log(error.response.data.message);
        });
    },*/
  },
  data() {
    return {
      activated: false,
    };
  },
};
</script>
