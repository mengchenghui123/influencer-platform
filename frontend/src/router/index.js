import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import TaskList from '../components/Tasks.vue';
import TaskDetail from '../components/TaskDetail.vue'; // 新增的 TaskDetail 组件
import UserProfile from '../components/Profile.vue';
import CreateTask from '../components/CreateTask.vue';
import MyTasks from '@/components/MyTasks.vue';
import MyApplications from '@/components/MyApplications.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: TaskList
  },
  {
    path: '/tasks/:id', // 任务详情页面
    name: 'TaskDetail',
    component: TaskDetail
  },
  {
    path: '/create-task', // 发布任务页面
    name: 'CreateTask',
    component: CreateTask
  },
  {
    path: '/profile',
    name: 'Profile',
    component: UserProfile,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/my-tasks',
    name: 'MyTasks',
    component: MyTasks,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/my-applications',
    name: 'MyApplications',
    component: MyApplications,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/login'
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
