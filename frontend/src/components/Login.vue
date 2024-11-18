<template>
  <div class="login-container d-flex justify-content-center align-items-center">
    <div class="login-card">
      <h2 class="text-center text-black">Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username" class="text-black">Username:</label>
          <input type="text" class="form-control" v-model="username" required />
        </div>
        <div class="form-group">
          <label for="password" class="text-black">Password:</label>
          <input type="password" class="form-control" v-model="password" required />
        </div>
        <button type="submit" class="btn btn-primary w-100 mt-3">Login</button>
      </form>
      <div v-if="errorMessage" class="alert alert-danger mt-3 text-center">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = window.location.hostname === 'localhost'
? 'http://127.0.0.1:8000'
: 'https://influencer-platform-uecu.onrender.com'

;

export default {
name: 'UserLogin',
data() {
  return {
    username: '',
    password: '',
    errorMessage: ''
  };
},
methods: {
  login() {
    axios
      .post(`${API_BASE_URL}/api/login/`, {
        username: this.username,
        password: this.password
      })
      .then((response) => {
        const token = response.data.access;
        localStorage.setItem('access_token', token);

        // Fetch user role to determine redirection
        axios
          .get(`${API_BASE_URL}/api/me/`, {
            headers: { Authorization: `Bearer ${token}` }
          })
          .then((res) => {
            const role = res.data.role;
            if (role === 'admin') {
              window.location.href = `${API_BASE_URL}/admin`;
            } else {
              this.$router.push('/tasks');
            }
          })
          .catch(() => {
            this.errorMessage = 'Failed to retrieve user role.';
          });
      })
      .catch(() => {
        this.errorMessage = 'Login failed. Please check your credentials.';
      });
  }
}
};
</script>

<style scoped>
/* Your CSS styling */
</style>
