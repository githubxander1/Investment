//
import Vue from 'vue';
import Router from 'vue-router';
import Calendar from '../components/Calendar.vue';
import Statistics from '../components/Statistics.vue';
import Search from '../components/Search.vue';
import YearView from '../components/YearView.vue'; // 假设 YearView 组件存在

import { createRouter, createWebHistory } from 'vue-router';
import { mapState } from 'vuex';
//
//
//Vue.use(Router);


import { createRouter, createWebHistory } from 'vue-router';
import Calendar from '../components/Calendar.vue'; // 确保路径正确
import AddSchedule from '../components/AddSchedule.vue'; // 添加日程页面
import EditSchedule from '../components/EditSchedule.vue'; // 编辑日程页面
import YearView from '../components/YearView.vue'; // 年视图页面

const routes = [
    {
        path: '/',
        name: 'Calendar',
        component: Calendar,
    },
    {
        path: '/add-schedule',
        name: 'AddSchedule',
        component: AddSchedule,
    },
    {
        path: '/edit/:scheduleId',
        name: 'EditSchedule',
        component: EditSchedule,
        props: true, // 自动将参数传递给组件
    },
    {
        path: '/year/:year',
        name: 'YearView',
        component: YearView,
        props: true, // 自动将参数传递给组件
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;











//const isAuthenticated = /* 检查用户是否已认证的逻辑 */;
//
//router.beforeEach((to, from, next) => {
//  //const isAuthenticated = /* 检查用户是否已认证 */;
//  if (to.meta.requiresAuth && !isAuthenticated) {
//    next('/login');
//  } else {
//    next();
//  }
//});


export default new Router({
  routes: [
    { path: '/', component: Calendar },
    { path: '/statistics', component: Statistics },
    { path: '/calendar', component: Calendar, name: 'calendar' },
    { path: '/year-view/:year', component: YearView, name: 'yearView' },
    { path: '/search', component: Search }
  ]
});