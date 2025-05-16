import { createRouter, createWebHistory } from 'vue-router'
import GetMyLocation from '../views/GetMyLocationView.vue'
import LocationMap from '@/views/LocationMapView.vue'
import GetLocationMap from '@/views/BasicMapView.vue'
import DiffCharView from '@/views/DiffCharView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: GetMyLocation,
    },
    {
      path: '/basic-map',
      name: 'basicMap',
      component: GetLocationMap,
    },
    {
      path: '/diff-char',
      name: 'diffChar',
      component: DiffCharView,
    },
    {
      path: '/location',
      name: 'location',
      component: LocationMap,
    },
  ],
})

export default router
