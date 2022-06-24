<template>
<div >
    <div>
      <h1>Tancar la sessió</h1>
      <b-button  variant="danger" @click="methodLogOut">Tancar</b-button>
    </div>
</div>
</template>

<script>
export default {
  name: 'LogOut',
  /*
      Defines the data used by the component
    */
  methods: {
    methodLogOut() {
      this.$router.replace({ path: '/' });
      this.$root.$emit('login', false);
    },
  },
};
</script>
