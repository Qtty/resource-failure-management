import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login'
import Admin from '../components/Admin'
import Responsable from '../components/Responsable'
import Resource from '../components/Resource'
import Etiquette from '../components/Etiquette'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  },
  {
    path: '/responsable',
    name: 'Responsable',
    component: Responsable
  },
  {
    path: '/resource/:_id',
    name: 'Resource',
    component: Resource
  },
  {
    path: '/etiquette/:_id',
    name: 'Etiquette',
    component: Etiquette
  },
  {
    path: '/',
    redirect: {
      name: 'Login'
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
