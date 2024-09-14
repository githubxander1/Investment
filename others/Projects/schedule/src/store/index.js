import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    schedules: JSON.parse(localStorage.getItem('schedules')) || []
  },
  mutations: {
      addSchedule(state, schedule) {
        state.schedules.push(schedule);
        this.$axios.post('/api/schedules', schedule).then(() => {
          localStorage.setItem('schedules', JSON.stringify(state.schedules));
        });
      },
      deleteSchedule(state, scheduleId) {
        state.schedules = state.schedules.filter(schedule => schedule.id !== scheduleId);
        this.$axios.delete(`/api/schedules/${scheduleId}`).then(() => {
          localStorage.setItem('schedules', JSON.stringify(state.schedules));
        });
      }
    }
  // 其他内容
});