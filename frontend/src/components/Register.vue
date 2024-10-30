<template>
    <div class="container">
      <h2>Registration</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" class="form-control" v-model="username" required>
        </div>
  
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" class="form-control" v-model="email" required>
        </div>
  
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" class="form-control" v-model="password" required>
        </div>
  
        <div class="form-group">
          <label for="firstName">First Name:</label>
          <input type="text" class="form-control" v-model="firstName" required>
        </div>
  
        <div class="form-group">
          <label for="lastName">Last Name:</label>
          <input type="text" class="form-control" v-model="lastName" required>
        </div>
  
        <div class="form-group">
          <label for="phone">Phone Number:</label>
          <input type="text" class="form-control" v-model="phoneNumber" required>
        </div>
  
        <div class="form-group">
          <label for="address">Address:</label>
          <textarea class="form-control" v-model="address" required></textarea>
        </div>
  
        <div class="form-group">
          <label for="role">Role:</label>
          <div class="select-wrapper">
            <select class="form-control role-select" v-model="role" required>
              <option value="">Select your role</option>
              <option value="merchant">Merchant</option>
              <option value="influencer">Influencer</option>
            </select>
          </div>
        </div>
  
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
  
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserRegister', // 保持多词命名
    data() {
      return {
        username: '',
        email: '',
        password: '',
        firstName: '',
        lastName: '',
        phoneNumber: '',
        address: '',
        role: '',
        errorMessage: ''
      };
    },
    methods: {
      register() {
        axios.post('http://127.0.0.1:8000/api/register/', {
          username: this.username,
          email: this.email,
          password: this.password,
          first_name: this.firstName, // 传递 firstName
          last_name: this.lastName,   // 传递 lastName
          phone_number: this.phoneNumber, // 传递 phoneNumber
          address: this.address,      // 传递 address
          role: this.role
        })
        .then(() => {
          this.$router.push('/login');
        })
        .catch(() => {
          this.errorMessage = 'Registration failed. Please try again.';
        });
      }
    }
  };
  </script>
  
  <style scoped>
  /* 控制角色选择框右侧的箭头 */
  .select-wrapper {
    position: relative;
  }
  
  .role-select {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    position: relative;
    width: 100%;
    padding-right: 30px; /* 确保箭头不会遮挡文本 */
  }
  
  .role-select::after {
    content: '▼'; /* 箭头 */
    position: absolute;
    top: 50%;
    right: 10px; /* 控制箭头位置 */
    transform: translateY(-50%);
    pointer-events: none;
  }
  </style>
  