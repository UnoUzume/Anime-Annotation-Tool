import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'

const app = createApp(App)
const win = window //
if (process.env.NODE_ENV === 'development') {
  if ('__VUE_DEVTOOLS_GLOBAL_HOOK__' in win) {
    // 这里__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue赋值一个createApp实例
    win.__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue = app
  }
}

app.use(ElementPlus)
app.mount('#app')
