<template>
  <div>
    <h1>Llistes de reproducció:</h1>
    <h6 style="max-width: 60%; margin: auto">
        Aquests botons serveixen per configurar la Raspberry sense haver-hi d'accedir físicament.
        Vés en compte a l'hora d'executar alguna d'aquestes instruccions.
      </h6>
    <div id="contentView" style="margin-top: 5%">


      <b-row style="padding-bottom:1.5%">
        <b-col cols="4" />
        <b-col cols="4" >
          <b-button class="btn-danger btn-block" v-on:click="executeScript(1)" data-toggle="tooltip" data-placement="right">
            Reiniciar Raspberry
          </b-button>
        </b-col>
        <b-col cols="4" />

      </b-row>
      <b-row style="padding-bottom:1.5%">
        <b-col cols="4" />
        <b-col cols="4" >
          <b-button class="btn-danger btn-block" v-on:click="executeScript(2)" data-toggle="tooltip" data-placement="right">
            Apagar Raspberry
          </b-button>
        </b-col>
        <b-col cols="4" />

      </b-row>
      <b-row style="padding-bottom:1.5%">
        <b-col cols="4" />
        <b-col cols="4" >
          <b-button class="btn-danger btn-block" v-on:click="executeScript(3)" data-toggle="tooltip" data-placement="right">
            Iniciar Billboard
          </b-button>
        </b-col>
        <b-col cols="4" />

      </b-row>
      <b-row  style="padding-bottom:1.5%">
        <b-col cols="4" />
        <b-col cols="4">
          <b-button class="btn-danger btn-block" v-on:click="executeScript(4)" data-toggle="tooltip" data-placement="right">
            Reiniciar Docker
          </b-button>
        </b-col>
        <b-col cols="4" />
      </b-row>
    </div>
  </div>
</template>

<script>
    import axios from "axios";

    export default {
      name: "Raspberry",
      data() {
        return {

        }
      },
      methods: {
        executeScript(script_mode) {
          let script = ""
          switch (script_mode) {
            case 1:
              script = 'shutdown -r now'
              break
            case 2:
              script = 'shutdown -h'
              break
            case 3:
              script = 'shutdown -h 19:57; ' +
                'docker-compose up -d ;chromium-browser --kiosk --app=localhost:8000\n'
              break
            case 4:
              script = 'sudo docker-compose stop; docker-compose down; docker-compose up \n'
              break
          }
          axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/script',
            data: {
              script: script,
            },
            auth: { username: this.$route.query.token },
          }).then((res) => {
            alert(res.data.message);
          })
            .catch((error) => {
              alert(error.response.data.message);
            });
          },
      }
    }
</script>

<style scoped>
</style>
