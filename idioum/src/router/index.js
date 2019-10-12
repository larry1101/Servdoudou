import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import indx from '@/components/indx'

Vue.use(Router)


export default new Router({
  routes: [
    {
      path: '/',
      name: 'indx',
      component: indx,
      children: [],
    },
    {
      path: '/hw',
      name: 'HelloWorld',
      component: HelloWorld,
    },
  ]
})
