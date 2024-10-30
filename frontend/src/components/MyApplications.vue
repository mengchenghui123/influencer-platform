<template>
    <div class="container my-5">
      <div class="card shadow-lg">
        <div class="card-header text-center bg-primary text-white">
          <h3 class="mb-0">My Applications</h3>
        </div>
        <div class="card-body">
          <div v-if="applications.length === 0">
            <p>No applications found.</p>
          </div>
          <table v-else class="table table-hover">
            <thead>
              <tr>
                <th>Task Name</th>
                <th>Status</th>
                <th>Applied Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="application in applications" :key="application.id">
                <td>{{ application.task }}</td>
                <td>{{ application.status }}</td>
                <td>{{ new Date(application.applied_at).toLocaleDateString() }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer text-center">
          <button @click="goToProfile" class="btn btn-secondary btn-sm">Back to Profile</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'MyApplications',
    data() {
      return {
        applications: [],
        errorMessage: '',
      };
    },
    mounted() {
      this.fetchApplications();
    },
    methods: {
      fetchApplications() {
        const token = localStorage.getItem('access_token');
        axios
          .get('http://127.0.0.1:8000/api/my-applied-tasks/', {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            this.applications = response.data;
          })
          .catch((error) => {
            this.errorMessage = 'Failed to fetch applications. Please try again.';
            console.error(error);
          });
      },
      goToProfile() {
        this.$router.push('/profile');
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
  }
  .card {
    border-radius: 10px;
  }
  .card-header {
    background-color: #007bff;
  }
  .btn-secondary {
    color: #fff;
    background-color: #6c757d;
    border: none;
  }
  .table-hover tbody tr:hover {
    background-color: #f5f5f5;
  }
  .alert {
    max-width: 800px;
    margin: auto;
  }
  </style>
  