<template>
  <div class="container my-5">
    <div class="card shadow-lg">
      <div class="card-header bg-primary text-white text-center">
        <h3 class="mb-0">Create New Task</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="createTask" enctype="multipart/form-data">
          <div class="form-group mb-3">
            <label for="title" class="form-label">Title</label>
            <input type="text" id="title" v-model="title" class="form-control" required />
          </div>
          <div class="form-group mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea id="description" v-model="description" class="form-control" required></textarea>
          </div>
          
          <!-- 文件上传部分 -->
          <div class="form-group mb-3">
            <label for="file" class="form-label">Upload File</label>
            <input type="file" id="file" @change="handleFileUpload" class="form-control" />
          </div>

          <!-- 图片上传部分 -->
          <div class="form-group mb-3">
            <label for="image" class="form-label">Upload Image</label>
            <input type="file" id="image" @change="handleImageUpload" class="form-control" />
          </div>
          
          <div class="form-group mb-3">
            <label for="budget" class="form-label">Budget</label>
            <input type="number" id="budget" v-model="budget" class="form-control" required />
          </div>
          <div class="form-group mb-3">
            <label for="deadline" class="form-label">Deadline</label>
            <input type="date" id="deadline" v-model="deadline" class="form-control" required />
          </div>
          
          <div class="d-flex justify-content-between">
            <button type="submit" class="btn btn-primary">Create Task</button>
            <button type="button" @click="goToTaskList" class="btn btn-secondary">Back to Task List</button>
          </div>
          <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
          <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = window.location.hostname === 'localhost'
? 'http://127.0.0.1:8000'
: 'https://influencer-platform-uecu.onrender.com';

export default {
  name: 'CreateTask',
  data() {
    return {
      title: '',
      description: '',
      budget: null,
      deadline: '',
      file: null,
      image: null,
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    handleImageUpload(event) {
      this.image = event.target.files[0];
    },
    createTask() {
      const token = localStorage.getItem('access_token');
      const formData = new FormData();
      formData.append('title', this.title);
      formData.append('description', this.description);
      formData.append('budget', this.budget);
      formData.append('deadline', this.deadline);

      if (this.file) {
        formData.append('file', this.file);
      }

      if (this.image) {
        formData.append('image', this.image);
      }

      axios
        .post(`${API_BASE_URL}/api/tasks/create/`, formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(() => {
          this.successMessage = 'Task created successfully!';
          this.errorMessage = '';
          this.resetForm();
        })
        .catch((error) => {
          console.error('Error creating task:', error);
          this.successMessage = '';
          this.errorMessage = 'Failed to create task. Please try again.';
        });
    },
    resetForm() {
      this.title = '';
      this.description = '';
      this.budget = null;
      this.deadline = '';
      this.file = null;
      this.image = null;
      this.errorMessage = '';
    },
    goToTaskList() {
      this.$router.push('/tasks');
    }
  }
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
  font-weight: bold;
}
.alert {
  margin-top: 1rem;
}
</style>
