import { createRouter, createWebHistory } from 'vue-router'
import LeaveRequest from '../components/LeaveRequest.vue'

const routes = [
  {
    path: '/leave-request',
    name: 'LeaveRequest',
    component: LeaveRequest
  },
  {
    path: '/',
    redirect: '/leave-request'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router