<template>
  <div class="year-view">
    <div class="header">
      <button @click="prevYear">Prev Year</button>
      <span>{{ currentYear }}</span>
      <button @click="nextYear">Next Year</button>
    </div>
    <div class="months">
      <div v-for="month in months" :key="month" @click="goToMonth(month)">
        {{ month }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentYear: new Date().getFullYear(),
      months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    };
  },
  methods: {
    prevYear() {
      this.currentYear--;
    },
    nextYear() {
      this.currentYear++;
    },
    goToMonth(monthIndex) {
      const newDate = new Date(this.currentDate.getFullYear(), monthIndex, 1);
      this.currentDate = newDate;
      this.$router.push({ name: 'calendar', params: { month: newDate.getMonth() + 1, year: newDate.getFullYear() } });
    }
  }
}
</script>