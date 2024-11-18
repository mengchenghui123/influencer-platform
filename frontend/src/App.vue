<template> 
  <div>
    <header>
      <h1>Influencer Platform</h1>
      <nav>
        <!-- 动态显示“Welcome, 角色 + 用户名” -->
        <span v-if="isLoggedIn">Welcome, {{ role }} {{ username }}</span>
        <div class="nav-links">
          <!-- 用户未登录时显示 Login 和 Register -->
          <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
          <router-link v-if="!isLoggedIn" to="/register">Register</router-link>
          <!-- 用户登录后显示 Profile 和 Logout -->
          <router-link v-if="isLoggedIn" to="/profile">Profile</router-link>
          <button v-if="isLoggedIn" @click="logout">Logout</button>
        </div>
      </nav>
    </header>

    <!-- 用于导航到登录、注册或其他页面的 Router 视图 -->
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = window.location.hostname === 'localhost'
? 'http://127.0.0.1:8000'
: 'https://influencer-platform-uecu.onrender.com'

;

export default {
  data() {
    return {
      isLoggedIn: !!localStorage.getItem('access_token'), // 检查登录状态
      username: localStorage.getItem('username') || '', // 从存储中获取用户名
      role: localStorage.getItem('role') || '', // 从存储中获取角色
      errorMessage: '',
    };
  },
  methods: {
    async login(username, password) {
      try {
        const response = await axios.post(`${API_BASE_URL}/api/login/`, {
          username: username,
          password: password,
        });
        const token = response.data.access;
        localStorage.setItem('access_token', token); // 保存令牌
        localStorage.setItem('username', username); // 保存用户名
        this.isLoggedIn = true; // 更新登录状态
        this.username = username;

        // 获取用户的角色信息
        await this.fetchUserRole();

        // 登录后重定向到任务页面
        this.$router.push('/tasks');
      } catch (error) {
        this.errorMessage = '登录失败，请检查您的凭据。';
      }
    },
    async fetchUserRole() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`${API_BASE_URL}/api/me/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.role = response.data.role; // 设置角色
        localStorage.setItem('role', this.role); // 保存角色到 localStorage
      } catch (error) {
        console.error('Error fetching user role:', error);
      }
    },
    logout() {
      localStorage.removeItem('access_token'); // 删除令牌
      localStorage.removeItem('username'); // 删除用户名
      localStorage.removeItem('role'); // 删除角色
      this.isLoggedIn = false; // 更新登录状态
      this.username = '';
      this.role = '';
      this.$router.push('/'); // 登出后返回主页面
    },
  },
  created() {
    // 在组件创建时验证登录状态，防止刷新后状态丢失
    this.isLoggedIn = !!localStorage.getItem('access_token');
    this.username = localStorage.getItem('username') || '';
    this.role = localStorage.getItem('role') || '';
    // 如果已登录但没有角色信息，尝试获取
    if (this.isLoggedIn && !this.role) {
      this.fetchUserRole();
    }
  }
};
</script>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f5f5f5;
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-links a,
.nav-links button {
  margin-left: 1rem;
  text-decoration: none;
  cursor: pointer;
  border: none;
  background: none;
  font: inherit;
  color: #007bff;
}

button {
  cursor: pointer;
}
</style>
