import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import store from './store.js'

const app = createApp(App)

//https://www.jianshu.com/p/5d03a8cadbc4
const win = window
if (process.env.NODE_ENV === 'development') {
  if ('__VUE_DEVTOOLS_GLOBAL_HOOK__' in win) {
    // 这里__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue赋值一个createApp实例
    win.__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue = app
  }
}
app.config.unwrapInjectedRef = true
app.use(store)
app.use(ElementPlus)
app.provide('host', 'http://127.0.0.1:5000')
app.mount('#app')