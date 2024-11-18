<template>
  <div>
    <header class="app-header">
      <div class="title-container">
        <h1>
          <router-link to="/" class="app-title">Influencer Platform</router-link>
        </h1>
        <div class="nav-main-links">
          <router-link to="/about" class="nav-link">About Us</router-link>
          <router-link to="/tasks" class="nav-link">Task</router-link>
          <router-link to="/contact" class="nav-link">Contact</router-link>
        </div>
      </div>
      <nav>
        <div class="nav-user-links">
          <span v-if="isLoggedIn">Welcome, {{ role }} {{ username }}</span>
          <router-link v-if="!isLoggedIn" to="/login" class="nav-link">Login</router-link>
          <router-link v-if="!isLoggedIn" to="/register" class="nav-link">Register</router-link>
          <router-link v-if="isLoggedIn" to="/profile" class="nav-link">Profile</router-link>
          <button v-if="isLoggedIn" @click="logout" class="nav-link">Logout</button>
        </div>
      </nav>
    </header>

    <div v-if="$route.path === '/'" class="about-content">
      <p>
        Welcome to the Influencer Platform. This is a space where businesses and
        influencers can collaborate seamlessly.
      </p>
    </div>

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
      isLoggedIn: !!localStorage.getItem("access_token"),
      username: localStorage.getItem("username") || "",
      role: localStorage.getItem("role") || "",
      errorMessage: "",
    };
  },
  methods: {
    async login(username, password) {
      try {
        const response = await axios.post(`${API_BASE_URL}/api/login/`, {
          username,
          password,
        });
        const token = response.data.access;
        localStorage.setItem("access_token", token);
        localStorage.setItem("username", username);
        this.isLoggedIn = true;
        this.username = username;
        await this.fetchUserRole();
        this.$router.push("/tasks");
      } catch (error) {
        this.errorMessage = "Login failed. Please check your credentials.";
      }
    },
    async fetchUserRole() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(`${API_BASE_URL}/api/me/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.role = response.data.role;
        localStorage.setItem("role", this.role);
      } catch (error) {
        console.error("Error fetching user role:", error);
      }
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("username");
      localStorage.removeItem("role");
      this.isLoggedIn = false;
      this.username = "";
      this.role = "";
      this.$router.push("/");
    },
  },
  created() {
    this.isLoggedIn = !!localStorage.getItem("access_token");
    this.username = localStorage.getItem("username") || "";
    this.role = localStorage.getItem("role") || "";
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
  background-color: white;
  border-bottom: 1px solid black;
}

.title-container {
  display: flex;
  align-items: center;
}

.app-title {
  text-decoration: none;
  color: black;
  cursor: pointer;
  margin-right: 2rem;
  font-size: 1.2rem;
}

.nav-main-links {
  display: flex;
  gap: 1rem;
}

.nav-main-links .nav-link,
.nav-user-links .nav-link {
  text-decoration: none;
  cursor: pointer;
  color: black;
  padding: 0.5rem 1rem;
  border: 1px solid black;
  border-radius: 8px;
  background-color: white;
  transition: box-shadow 0.3s ease, background-color 0.3s ease;
}

.nav-main-links .nav-link:hover,
.nav-user-links .nav-link:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  background-color: #f8f8f8;
}

.nav-user-links {
  display: flex;
  gap: 1rem;
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
