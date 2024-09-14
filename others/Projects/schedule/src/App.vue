<template>
  <div id="app">根app
    <TabBar />
    <router-view />
  </div>
</template>

<script>
import TabBar from './components/TabBar.vue';

export default {
  components: {
    TabBar
  }
}
</script>