import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000/api'

store.dispatch("restore")
  .catch(err => console.warn(err))
  .finally(() => {
    const app = createApp(App)
    app.use(store)
    app.use(router)
    app.mount('#app')
  })