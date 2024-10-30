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
          .post('http://127.0.0.1:8000/api/login/', {
            username: this.username,
            password: this.password
          })
          .then((response) => {
            const token = response.data.access;
            localStorage.setItem('access_token', token);
  
            // Fetch user role to determine redirection
            axios
              .get('http://127.0.0.1:8000/api/me/', {
                headers: { Authorization: `Bearer ${token}` }
              })
              .then((res) => {
                const role = res.data.role;
                if (role === 'admin') {
                  window.location.href = 'http://127.0.0.1:8000/admin';
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
  .login-container {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #fafafa; /* 蓝色背景 */
  }
  
  .login-card {
    width: 300px;
    padding: 2rem;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    margin-bottom: 1.5rem;
    color: #ffffff;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .btn-primary {
    background-color: #0056b3;
    border: none;
  }
  
  .btn-primary:hover {
    background-color: #004085;
  }
  </style>
  