<template>
    <div class="container my-5">
      <div class="card text-white bg-primary shadow-lg">
        <div class="card-header text-center">
          <h3 class="mb-0">User Profile</h3>
        </div>
        <div class="card-body">
          <div v-if="user">
            <p><strong>Username:</strong> {{ user.username }}</p>
            <p><strong>First Name:</strong> {{ user.first_name }}</p>
            <p><strong>Last Name:</strong> {{ user.last_name }}</p>
            <p><strong>Role:</strong> {{ user.role }}</p>
            <p v-if="user.phone_number"><strong>Phone Number:</strong> {{ user.phone_number }}</p>
            <p v-if="user.address"><strong>Address:</strong> {{ user.address }}</p>
          </div>
          <div v-else>
            <p>Loading...</p>
          </div>
        </div>
        <div class="card-footer text-center">
          <button v-if="isMerchant" @click="goToMyTasks" class="btn btn-light btn-sm">My Tasks</button>
          <button v-else @click="goToMyApplications" class="btn btn-light btn-sm">My Applications</button>
          <button @click="goToTaskList" class="btn btn-secondary btn-sm">Back to Task List</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserProfile',
    data() {
      return {
        user: null,
        isMerchant: false,
      };
    },
    mounted() {
      this.fetchUserProfile();
    },
    methods: {
      fetchUserProfile() {
        const accessToken = localStorage.getItem('access_token');
        axios
          .get('http://127.0.0.1:8000/api/me/', {
            headers: { Authorization: `Bearer ${accessToken}` },
          })
          .then((response) => {
            this.user = response.data;
            this.isMerchant = this.user.role === 'merchant';
          })
          .catch(() => {
            alert('Error fetching profile.');
            this.$router.push('/login');
          });
      },
      goToMyTasks() {
        this.$router.push('/my-tasks');
      },
      goToMyApplications() {
        this.$router.push('/my-applications');
      },
      goToTaskList() {
        this.$router.push('/tasks');
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  .card {
    border-radius: 10px;
  }
  .card-header {
    background-color: #007bff;
  }
  .card-body p {
    margin: 0.5rem 0;
  }
  .btn-light {
    color: #007bff;
    font-weight: bold;
  }
  </style>
  