// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import 'muse-ui/dist/muse-ui.css';
import 'muse-ui-loading/dist/muse-ui-loading.css'; // load css

import Vue from 'vue'
import App from './App'
import router from './router'

import MuseUI from 'muse-ui';
Vue.use(MuseUI);
import Loading from 'muse-ui-loading';
Vue.use(Loading);
import Toast from 'muse-ui-toast';
Vue.use(Toast);

// import { Uploader } from 'vant';
// import 'vant/lib/uploader/style';
// Vue.use(Uploader);

import { Upload } from 'element-ui';
Vue.use(Upload)

import 'typeface-roboto'

import axios from 'axios'
import qs from 'qs'

Vue.prototype.$axios = axios;
Vue.prototype.$qs = qs

Vue.config.productionTip = false


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
