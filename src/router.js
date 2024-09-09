import Vue from 'vue';
import VueRouter from 'vue-router';

import { jwtDecode } from 'jwt-decode';

import Login from './views/LoginView.vue';
import UserDashboard from './views/UserDashboard.vue';
import AdminDashboard from './views/AdminDashboard.vue';
import ManageEmployees from './views/ManageEmployees.vue';
import LeaveRequests from './views/LeaveRequests.vue';
import UserCalendar from './views/UserCalendar.vue';
import LeaveApplication from './views/LeaveApplication.vue';
import UserInfo from './views/UserInfo.vue';

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
    meta: { requiresAuth: true },  // Protect this route
    children: [
      {
        path: 'calendar',
        name: 'UserCalendar',
        component: UserCalendar,
        meta: { requiresAuth: true }  // Protect this route
      },
      {
        path: 'leave-application',
        name: 'LeaveApplication',
        component: LeaveApplication,
        meta: { requiresAuth: true }  // Protect this route
      },
      {
        path: 'info',
        name: 'UserInfo',
        component: UserInfo,
        meta: { requiresAuth: true }  // Protect this route
      }
    ]
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true },  // Protect this route
    children: [
      {
        path: 'manage-employees',
        name: 'ManageEmployees',
        component: ManageEmployees,
        meta: { requiresAuth: true }  // Protect this route
      },
      {
        path: 'leave-requests',
        name: 'LeaveRequests',
        component: LeaveRequests,
        meta: { requiresAuth: true }  // Protect this route
      }
    ]
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});


router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem('token'); // Get the token from localStorage

  console.log('Navigating to:', to.fullPath);
  console.log('From:', from.fullPath);
  console.log('Token:', token);

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      console.log('No token found, redirecting to login');
      // No token, redirect to login
      next({
        path: '/',
        replace: true
      });
    } else {
      try {
        // Decode and check token validity
        console.log(token)
        const decoded = jwtDecode(token,);
        const now = Math.floor(Date.now() / 1000);

        console.log('Token decoded:', decoded);
        console.log('Current time:', now);
        console.log('Token expiration time:', decoded.exp);

        if (decoded.exp < now) {
          console.log('Token is expired, removing token and redirecting to login');
          // Token is expired
          sessionStorage.removeItem('token');
          next({
            path: '/',
            replace: true
          });
        } else {
          console.log('Token is valid, proceeding to route');
          // Token is valid
          next();  // Proceed to the route
        }
      } catch (e) {
        console.log('Error decoding token, removing token and redirecting to login');
        console.log(e)
        // Error decoding token
        sessionStorage.removeItem('token');
        next({
          path: '/',
          replace: true
        });
      }
    }
  } else {
    console.log('No authentication required for this route');
    next(); // Make sure to always call next()
  }
});




export default router;
