import Vue from 'vue';
import Router from 'vue-router';
// import Books from './components/Books.vue';
import Ping from './components/Ping.vue';
import Webapp from './components/Webapp.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/',
      name: 'mv_asc',
      component: Webapp,
    },
  ],
});
