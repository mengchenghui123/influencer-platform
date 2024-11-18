<template>
  <div>
    <header class="app-header">
      <div class="title-container">
        <h1>
          <router-link to="/" class="app-title">Influencer Platform</router-link>
        </h1>
        <div class="nav-main-links-container">
          <div class="nav-main-links">
            <router-link to="/about">About Us</router-link>
            <router-link to="/tasks">Task</router-link>
            <router-link to="/contact">Contact</router-link>
          </div>
        </div>
      </div>
      <nav>
        <div class="nav-user-links">
          <!-- 动态显示“Welcome, 角色 + 用户名” -->
          <span v-if="isLoggedIn">Welcome, {{ role }} {{ username }}</span>
          <!-- 用户未登录时显示 Login 和 Register -->
          <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
          <router-link v-if="!isLoggedIn" to="/register">Register</router-link>
          <!-- 用户登录后显示 Profile 和 Logout -->
          <router-link v-if="isLoggedIn" to="/profile">Profile</router-link>
          <button v-if="isLoggedIn" @click="logout">Logout</button>
        </div>
      </nav>
    </header>

    <!-- 如果是主界面则显示默认内容 -->
    <div v-if="$route.path === '/'" class="about-content">
      <p>
        Welcome to the Influencer Platform. This is a space where businesses and
        influencers can collaborate seamlessly.
      </p>
    </div>

    <!-- 如果不是主界面，则显示 Router 视图 -->
    <router-view v-else></router-view>
  </div>
</template>

<script>
import axios from "axios";

const API_BASE_URL =
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000"
    : "https://influencer-platform-uecu.onrender.com";

export default {
  data() {
    return {
      isLoggedIn: !!localStorage.getItem("access_token"), // 检查登录状态
      username: localStorage.getItem("username") || "", // 从存储中获取用户名
      role: localStorage.getItem("role") || "", // 从存储中获取角色
      errorMessage: "",
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
        localStorage.setItem("access_token", token); // 保存令牌
        localStorage.setItem("username", username); // 保存用户名
        this.isLoggedIn = true; // 更新登录状态
        this.username = username;

        // 获取用户的角色信息
        await this.fetchUserRole();

        // 登录后重定向到任务页面
        this.$router.push("/tasks");
      } catch (error) {
        this.errorMessage = "登录失败，请检查您的凭据。";
      }
    },
    async fetchUserRole() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(`${API_BASE_URL}/api/me/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.role = response.data.role; // 设置角色
        localStorage.setItem("role", this.role); // 保存角色到 localStorage
      } catch (error) {
        console.error("Error fetching user role:", error);
      }
    },
    logout() {
      localStorage.removeItem("access_token"); // 删除令牌
      localStorage.removeItem("username"); // 删除用户名
      localStorage.removeItem("role"); // 删除角色
      this.isLoggedIn = false; // 更新登录状态
      this.username = "";
      this.role = "";
      this.$router.push("/"); // 登出后返回主页面
    },
  },
  created() {
    // 在组件创建时验证登录状态，防止刷新后状态丢失
    this.isLoggedIn = !!localStorage.getItem("access_token");
    this.username = localStorage.getItem("username") || "";
    this.role = localStorage.getItem("role") || "";
    // 如果已登录但没有角色信息，尝试获取
    if (this.isLoggedIn && !this.role) {
      this.fetchUserRole();
    }
  },
};
</script>

<style scoped>
/* Header 样式 */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #007bff;
  color: white;
}

.title-container {
  display: flex;
  align-items: center;
}

.app-title {
  text-decoration: none;
  color: white;
  cursor: pointer;
  margin-right: 2rem;
}

.nav-main-links-container {
  border: 2px solid white;
  padding: 0.5rem;
  border-radius: 8px;
}

.nav-main-links {
  display: flex;
  gap: 1rem;
}

.nav-user-links {
  display: flex;
  gap: 1rem;
}

.nav-main-links a,
.nav-user-links a,
.nav-user-links button {
  text-decoration: none;
  cursor: pointer;
  border: none;
  background: none;
  font: inherit;
  color: white;
}

button {
  cursor: pointer;
}

/* About Content 样式 */
.about-content {
  padding: 2rem;
  margin: 2rem auto;
  text-align: center;
  border: 2px solid #007bff;
  border-radius: 8px;
  width: 70%;
  background-color: #f0f8ff;
}

.about-content p {
  font-size: 1rem;
  line-height: 1.6;
  color: #333;
}
</style>
