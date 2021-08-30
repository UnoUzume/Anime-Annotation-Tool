import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  // alias: {
  //   vue: 'vue/dist/vue.esm-bundler.js', // 定义vue的别名，如果使用其他的插件，可能会用到别名
  // },
  plugins: [vue()],
  build: {
    // rollupOptions: {
    //   output: {
    //     //https://blog.csdn.net/weixin_41277748/article/details/116431789
    //     //解决打包时Some chunks are larger警告
    //     manualChunks(id) {
    //       if (id.includes('node_modules')) {
    //         return id
    //           .toString()
    //           .split('node_modules/')[1]
    //           .split('/')[0]
    //           .toString()
    //       }
    //     },
    //   },
    // },
    chunkSizeWarningLimit: 1500,
  },
})
