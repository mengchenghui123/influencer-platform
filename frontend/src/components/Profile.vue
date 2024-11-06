<template>
    <div class="container my-5">
      <div class="card text-white bg-primary shadow-lg">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h3 class="mb-0">User Profile</h3>
          <button
            v-if="!isEditing"
            @click="toggleEditMode"
            class="btn btn-light btn-sm"
          >
            Edit Profile
          </button>
        </div>
        <div class="card-body">
          <div v-if="user">
            <div v-if="!isEditing">
              <p><strong>Username:</strong> {{ user.username }}</p>
              <p><strong>First Name:</strong> {{ user.first_name }}</p>
              <p><strong>Last Name:</strong> {{ user.last_name }}</p>
              <p><strong>Role:</strong> {{ user.role }}</p>
              <p v-if="user.phone_number"><strong>Phone Number:</strong> {{ user.phone_number }}</p>
              <p v-if="user.address"><strong>Address:</strong> {{ user.address }}</p>
            </div>
  
            <div v-else>
              <div class="form-group mb-3">
                <label for="firstName">First Name</label>
                <input
                  type="text"
                  id="firstName"
                  v-model="user.first_name"
                  class="form-control"
                />
              </div>
              <div class="form-group mb-3">
                <label for="lastName">Last Name</label>
                <input
                  type="text"
                  id="lastName"
                  v-model="user.last_name"
                  class="form-control"
                />
              </div>
              <div class="form-group mb-3">
                <label for="phone">Phone Number</label>
                <input
                  type="text"
                  id="phone"
                  v-model="user.phone_number"
                  class="form-control"
                />
              </div>
              <div class="form-group mb-3">
                <label for="address">Address</label>
                <textarea
                  id="address"
                  v-model="user.address"
                  class="form-control"
                ></textarea>
              </div>
            </div>
          </div>
          <div v-else>
            <p>Loading...</p>
          </div>
        </div>
        <div class="card-footer text-center">
          <button
            v-if="isEditing"
            @click="saveProfile"
            class="btn btn-success btn-sm"
          >
            Save
          </button>
          <button
            v-if="isEditing"
            @click="cancelEdit"
            class="btn btn-secondary btn-sm"
          >
            Cancel
          </button>
          <button
            v-if="!isEditing && isMerchant"
            @click="goToMyTasks"
            class="btn btn-light btn-sm"
          >
            My Tasks
          </button>
          <button
            v-if="!isEditing && !isMerchant"
            @click="goToMyApplications"
            class="btn btn-light btn-sm"
          >
            My Applications
          </button>
          <button @click="goToTaskList" class="btn btn-secondary btn-sm">Back to Task List</button>
        </div>
      </div>
      <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
      <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
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
        isEditing: false,
        successMessage: '',
        errorMessage: '',
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
      toggleEditMode() {
        this.isEditing = true;
      },
      saveProfile() {
        const accessToken = localStorage.getItem('access_token');
        axios
          .put(
            'http://127.0.0.1:8000/api/update-profile/',
            {
              first_name: this.user.first_name,
              last_name: this.user.last_name,
              phone_number: this.user.phone_number,
              address: this.user.address,
            },
            {
              headers: { Authorization: `Bearer ${accessToken}` },
            }
          )
          .then(() => {
            this.successMessage = 'Profile updated successfully!';
            this.errorMessage = '';
            this.isEditing = false;
          })
          .catch((error) => {
            this.errorMessage = 'Failed to update profile. Please try again.';
            console.error(error);
          });
      },
      cancelEdit() {
        this.fetchUserProfile();
        this.isEditing = false;
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
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .card-body p,
  .form-group {
    margin: 0.5rem 0;
  }
  .btn-light {
    color: #007bff;
    font-weight: bold;
  }
  </style>
  