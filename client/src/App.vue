<template>
  <div id="app">
    <b-navbar variant="faded" type="dark">
      <b-navbar-brand>
        <img src="https://campusvirtual.ub.edu/pluginfile.php/1/theme_snap/logo/1655335259/ub_logo.png"
             height="35"
             class="d-inline-block align-top" alt="Logo UB" style="margin-right: 1rem"
        href="https://mat.ub.edu/">
        Gestió de la cartellera
      </b-navbar-brand>
    </b-navbar>

    <router-view/>
    <b-navbar variant="faded" fixed="bottom" small>
      <div style="margin: 0px auto">
        <img src="../static/crai_logo_unatinta_blanc.png" width="250" height="80">
      <b-button v-b-modal.about-modal style="color:white;width:300px; height:80px"
                variant="link">Sobre aquesta aplicació</b-button>
      <img src="../static/logo_ub.png" width="250" height="80">
      </div>

    </b-navbar>
    <b-modal class="modal-backdrop fade in"  hide-backdrop id="about-modal" hide-footer>
      <label style="display: flex; margin-bottom: .5rem;color: #0072ce;">
        Projecte desenvolupat com a Treball de Final de Grau d'Enginyeria Informàtica
        (Universitat de Barcelona)
      </label>
      <label style="display: flex; margin-bottom: .5rem;color: #0072ce;">Llicència: GPL 3</label>
      <label style="display: flex; margin-bottom: .5rem;color: #0072ce;">
        © Francina Pons Llabrés 2022</label>
      <label style="display: flex; margin-bottom: .5rem;color: #0072ce;">
        Contacte: fponsllabres@gmail.com</label>
      <b-link href="https://github.com/francinaPons" style="display: flex; margin-bottom: .5rem;color: #0072ce;" >Github</b-link>
    </b-modal>
  </div>
</template>

<style>
#app {
  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

</style>
