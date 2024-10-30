import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // 确保导入了路由
import 'bootstrap/dist/css/bootstrap.css';

const app = createApp(App);

app.use(router); // 使用路由器
app.mount('#app'); // 挂载 Vue 实例