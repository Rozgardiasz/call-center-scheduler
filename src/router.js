// src/router/index.js
import Vue from 'vue';
import VueRouter from 'vue-router';
import Login from './/views/LoginView.vue';
import UserDashboard from './/views/UserDashboard.vue';
import AdminDashboard from './/views/AdminDashboard.vue';
import ManageEmployees from './/views/ManageEmployees.vue';
import LeaveRequests from './/views/LeaveRequests.vue';
import UserCalendar from './/views/UserCalendar.vue';
import LeaveApplication from './/views/LeaveApplication.vue';
import UserInfo from './/views/UserInfo.vue';


Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/user-dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    children: [
      {
        path: 'calendar',
        name: 'UserCalendar',
        component: UserCalendar
      },
      {
        path: 'leave-application',
        name: 'LeaveApplication',
        component: LeaveApplication
      },
      {
        path: 'info',
        name: 'UserInfo',
        component: UserInfo
      }

    ]
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    children: [
      {
        path: 'manage-employees',
        name: 'ManageEmployees',
        component: ManageEmployees
      },
      {
        path: 'leave-requests',
        name: 'LeaveRequests',
        component: LeaveRequests
      }
    ]
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
