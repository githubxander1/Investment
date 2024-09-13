<template>
  <div class="calendar">
    <!-- 日历头部 -->
    <div class="header">
      <!-- 上一个月按钮 -->
      <button @click="prevMonth">Prev</button>
      <!-- 当前显示的月份和年份 -->
      <span>{{ currentMonth }} {{ currentYear }}</span>
      <!-- 下一个月按钮 -->
      <button @click="nextMonth">Next</button>
    </div>
    <!-- 显示周数 -->
    <div class="weeks">
      <div v-for="week in weeks" :key="week">
        {{ week }}
      </div>
    </div>
    <!-- 显示一周中的每一天 -->
    <div class="days">
      <div v-for="day in daysOfWeek" :key="day">{{ day }}</div>
    </div>
    <!-- 显示具体日期 -->
    <div class="dates">
      <div v-for="date in dates" :key="date.date" :class="{ today: isToday(date), hasSchedule: hasSchedule(date) }" @click="selectDate(date)">
        {{ date.day }}
      </div>
    </div>
    <!-- 添加日程按钮 -->
    <button @click="goToAddSchedule">Add Schedule</button>

    <!-- 为日程添加分类和优先级字段，并在日程列表中展示这些信息。 -->
    <div class="schedule-details" v-if="selectedDate">
      <h3>Schedule for {{ selectedDate.toLocaleDateString() }}</h3>
      <ul>
        <li v-for="schedule in selectedSchedules" :key="schedule.id">
          {{ schedule.title }} - {{ schedule.category }} - {{ schedule.priority }}
        </li>
      </ul>
    </div>
    <!-- 编辑已有日程的功能 -->
    <div class="schedule-details" v-if="selectedDate">
      <ul>
        <li v-for="schedule in selectedSchedules" :key="schedule.id">
          {{ schedule.title }} - {{ schedule.date }}
          <button @click="editSchedule(schedule)">Edit</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';


export default {
  data() {
    return {
      selectedDate: null,
      currentDate: new Date(), // 初始化当前日期
      daysOfWeek: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] // 一周七天的缩写
    };
  },
  computed: {
    ...mapState(['schedules']), // 从 Vuex store 获取 schedules 数据
    // selectedSchedules() {
      // return this.schedules.filter(schedule =>
       //  schedule.date.toDateString() === this.selectedDate.toDateString()
      ); // 根据日期过滤出当前选中日期的日程
    currentYear() { // 计算当前年份
      return this.currentDate.getFullYear();
    },
    currentMonth() { // 计算当前月份
      return this.currentDate.toLocaleString('default', { month: 'long' });
    },
    dates() { // 计算当月的所有日期
      const dates = [];
      const firstDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1).getDay(); // 获取当月第一天是星期几
      const lastDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0).getDate(); // 获取当月最后一天
      // 添加空白格子
      for (let i = 0; i < firstDay; i++) {
        dates.push({ day: '' });
      }
      // 添加实际日期
      for (let i = 1; i <= lastDay; i++) {
        const date = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), i);
        dates.push({ date, day: i });
      }
      return dates;
    },
    computedWeeks() { // 计算周数  // 修改属性名以避免冲突
      const firstDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1).getDay();
      const lastDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0).getDate();
      const weeks = Math.ceil((lastDay + firstDay - 1) / 7);
      const weekArray = Array.from({ length: weeks }, (_, index) => `Week ${index + 1}`);
      return weekArray;
    }
  },
  methods: { //方法逻辑
    prevMonth() { // 切换到上一个月
      this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() - 1, 1);
    },
    nextMonth() { // 切换到下一个月
      this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 1);
    },
    isToday(date) { // 判断给定日期是否为今天
      const today = new Date();
      return date.date.getFullYear() === today.getFullYear() &&
             date.date.getMonth() === today.getMonth() &&
             date.date.getDate() === today.getDate();
    },
    hasSchedule(date) { // 检查给定日期是否有日程安排
      return this.schedules.some(schedule => schedule.date.toDateString() === date.date.toDateString());
    },
    selectDate(date) { // 处理日期选择逻辑，例如跳转到日程详情页面
      this.selectedDate = date.date;// 可以在这里添加具体的逻辑
    },
    goToAddSchedule() { // 跳转到添加日程页面
      this.$router.push('/add-schedule');
    },
    switchToYearView() { //从当前视图（假设是月视图）切换到年视图的逻辑
      const newDate = new Date(this.currentDate.getFullYear(), 0, 1); // 设置为当前年份的第一天
      this.currentDate = newDate;
      this.$router.push({ name: 'yearView', params: { year: newDate.getFullYear() } });
    },
    editSchedule(schedule) {
      this.$router.push({ name: 'edit', params: { scheduleId: schedule.id } });
    }
  }
}
</script>

<style>
.calendar .today { // 今天的日期背景颜色
  background-color: yellow;
}
.calendar .hasSchedule { // 有日程安排的日期字体颜色
  color: red;
}
</style>
