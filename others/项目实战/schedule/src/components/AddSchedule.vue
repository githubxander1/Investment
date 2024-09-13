<template>
  <div class="add-schedule">
    <h3>Add Schedule</h3>
    <form @submit.prevent="saveSchedule">
      <input v-model="schedule.title" placeholder="Title" required>
      <textarea v-model="schedule.content" placeholder="Content"></textarea>
      <select v-model="schedule.time">
        <!-- 时间选项 -->
      </select>
      <button type="submit">Save</button>
      <button type="button" @click="deleteSchedule" v-if="schedule.id">Delete</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      schedule: {
        id: null,
        title: '',
        content: '',
        time: '',
        date: new Date()
        repeat: 'none', // 可以是 'none', 'daily', 'weekly', 'monthly', 'yearly'
        repeatCount: 1 // 重复次数
      }
    };
  },
  methods: {
  async saveSchedule() { //保存日程逻辑
    try {
      const response = await axios.post('/api/schedules', this.schedule);
      this.$store.commit('addSolution', response.data);//确保所有的数据操作都与后端API同步，包括错误处理和数据验证。
      this.resetForm();
      this.schedule.reminder = this.calculateReminderTime();
      this.scheduleNotifications();
      this.schedule.repeat = this.schedule.repeat || 'none';
      this.schedule.repeatCount = this.schedule.repeatCount || 1;
      this.resetForm();
      this.$emit('save', this.schedule);

      this.$store.commit('addSchedule', response.data);
      this.$emit('save', response.data);
      this.resetForm();
    } catch (error) {
          console.error('Error saving schedule:', error);
          logError(error); // 添加错误日志记录
          alert('Failed to save schedule. Please try again.');
        }
  },
  async deleteSchedule() {
    try {
      await axios.delete(`/api/schedules/${this.schedule.id}`);
      this.$store.commit('deleteSolution', this.schedule.id);
      this.$emit('delete', this.schedule.id);
      this.resetForm();
    } catch (error) {
      console.error('Error deleting schedule:', error);
      alert('Failed to delete schedule. Please try again.');
    }
  },
  calculateReminderTime() {
      const now = new Date();
      const reminderTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), now.getMinutes() - 15);
      return reminderTime;
    },
  scheduleNotifications() {
      const reminderTime = this.calculateReminderTime();
      const now = new Date();
      const timeUntilReminder = reminderTime - now;

      if (timeUntilReminder > 0) {
        setTimeout(() => {
          showNotification('Reminder', { body: `Your event "${this.schedule.title}" is starting soon.` });
        }, timeUntilReminder);
      }
    },
  editSchedule(schedule) {
      this.$router.push({ name: 'edit', params: { scheduleId: schedule.id } });
    }
}
}
</script>