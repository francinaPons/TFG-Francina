import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import VueGoodTablePlugin from 'vue-good-table';
import 'vue-good-table/dist/vue-good-table.css';
import VueTaggableSelect from 'vue-taggable-select';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';
import './assets/application.css';
import BootstrapVueIcons from "bootstrap-vue/dist/bootstrap-vue-icons.esm";

Vue.component('vue-taggable-select', VueTaggableSelect);

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons)
Vue.use(VueGoodTablePlugin);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
