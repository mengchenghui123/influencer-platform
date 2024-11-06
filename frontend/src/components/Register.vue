<template>
    <div class="register-container d-flex justify-content-center align-items-center">
      <div class="register-card card shadow-lg">
        <div class="card-header text-center bg-primary text-white">
          <h3 class="mb-0">Registration</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="register">
            <div class="form-group mb-3">
              <label for="username">Username:</label>
              <input type="text" class="form-control" v-model="username" required />
            </div>
    
            <div class="form-group mb-3">
              <label for="email">Email:</label>
              <input type="email" class="form-control" v-model="email" required />
            </div>
    
            <div class="form-group mb-3">
              <label for="password">Password:</label>
              <input type="password" class="form-control" v-model="password" required />
            </div>
    
            <div class="form-group mb-3">
              <label for="firstName">First Name:</label>
              <input type="text" class="form-control" v-model="firstName" required />
            </div>
    
            <div class="form-group mb-3">
              <label for="lastName">Last Name:</label>
              <input type="text" class="form-control" v-model="lastName" required />
            </div>
    
            <div class="form-group mb-3">
              <label for="phone">Phone Number:</label>
              <input type="text" class="form-control" v-model="phoneNumber" required />
            </div>
    
            <div class="form-group mb-3">
              <label for="address">Address:</label>
              <textarea class="form-control" v-model="address" required></textarea>
            </div>
    
            <div class="form-group mb-3">
              <label for="role">Role:</label>
              <div class="select-wrapper">
                <select class="form-control role-select" v-model="role" required>
                  <option value="">Select your role</option>
                  <option value="merchant">Merchant</option>
                  <option value="influencer">Influencer</option>
                </select>
              </div>
            </div>
    
            <button type="submit" class="btn btn-primary w-100">Register</button>
          </form>
    
          <div v-if="errorMessage" class="alert alert-danger mt-3 text-center">
            {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserRegister',
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
          first_name: this.firstName,
          last_name: this.lastName,
          phone_number: this.phoneNumber,
          address: this.address,
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
  .register-container {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .register-card {
    width: 350px;
    border-radius: 8px;
  }
  
  .card-header {
    background-color: #007bff;
    color: #fff;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .select-wrapper {
    position: relative;
  }
  
  .role-select {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    padding-right: 30px;
  }
  
  .role-select::after {
    content: '▼';
    position: absolute;
    top: 50%;
    right: 10px;
    transform: translateY(-50%);
    pointer-events: none;
  }
  
  .btn-primary {
    background-color: #007bff;
    border: none;
  }
  
  .btn-primary:hover {
    background-color: #0056b3;
  }
  </style>
  