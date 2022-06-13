<template>
  <v-app>
    <v-main>
      <List/>
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import List from './components/List.vue'

export default {
  name: 'App',

  components: {
    HelloWorld,
    List
  },

  data: () => ({
    //
  }),
}
</script>
