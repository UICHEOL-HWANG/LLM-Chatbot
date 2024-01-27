import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import 'nes.css/css/nes.min.css';
import './assets/fonts.css'; // 웹폰트 CSS 파일 임포트


Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
