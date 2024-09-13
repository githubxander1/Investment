<template>
  <div class="tab-bar">
    <button @click="selectTab('calendar')">日历</button>
    <button @click="selectTab('statistics')">统计</button>
    <button @click="selectTab('search')">搜索</button>
  </div>
</template>

<script>
export default {
  methods: {
    selectTab(tab) {
      this.$store.commit('setActiveTab', tab);
    }
  }
}
</script>

<style>
.tab-bar button {
  margin-right: 10px;
}
</style>