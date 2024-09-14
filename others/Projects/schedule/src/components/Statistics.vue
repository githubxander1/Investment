<template>
  <div class="statistics">
    <h3>Total Schedules: {{ totalSchedules }}</h3>
    <h3>Tags Statistics:</h3>
    <ul>
      <li v-for="(count, tag) in tagStatistics" :key="tag">
        {{ tag }}: {{ count }}
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState(['schedules']),
    totalSchedules() {
      return this.schedules.length;
    },
    tagStatistics() {
      const tags = {};
      this.schedules.forEach(schedule => {
        schedule.tags.forEach(tag => {
          if (!tags[tag]) {
            tags[tag] = 0;
          }
          tags[tag]++;
        });
      });
      return tags;
    }
  }
}
</script>