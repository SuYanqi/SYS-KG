import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import 'bootstrap/dist/css/bootstrap.css';
import '../public/css/bootstrap.min.css';
import '../public/css/ress.css';



import ElementPlus from 'element-plus'
// import * as Icon from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'

// createApp(App).use(store).use(router).use(ElementPlus).use(Icon).mount("#app");
createApp(App).use(store).use(router).use(ElementPlus).mount("#app");

