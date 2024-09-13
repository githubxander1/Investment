<template>
  <div class="search">
    <input v-model="searchQuery" placeholder="Search schedules...">
    <ul>
      <li v-for="schedule in filteredSchedules" :key="schedule.id">
        {{ schedule.title }} - {{ schedule.date }}
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } = require('vuex');

export default {
  data() {
    return {
      searchQuery: ''
    };
  },
  computed: {
    ...mapState(['schedules']),
    filteredSchedules() {
      return this.schedules.filter(schedule =>
        schedule.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        schedule.content.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  }
}
</script>