<template>
    <div class="container my-5">
      <div class="card text-white bg-primary shadow-lg">
        <div class="card-header text-center">
          <h3 class="mb-0">{{ task?.title || 'Task Details' }}</h3>
        </div>
        <div class="card-body">
          <div v-if="task">
            <p><strong>Description:</strong> {{ task.description }}</p>
            <p><strong>Budget:</strong> {{ task.budget }}</p>
            <p><strong>Deadline:</strong> {{ task.deadline }}</p>
            <p><strong>Posted by:</strong> {{ task.posted_by }}</p>
  
            <!-- Attachment Section -->
            <div class="mt-3">
              <p><strong>Attachment:</strong></p>
  
              <!-- 显示图片 -->
              <div v-if="task.image" class="mt-2">
                <img :src="task.image" alt="Task Image" class="img-fluid mb-3" />
              </div>
  
              <!-- 文件下载链接 -->
              <div v-if="task.file" class="mt-2">
                <a :href="task.file" download class="btn btn-light text-primary btn-sm">
                  Download File
                </a>
              </div>
  
              <!-- 没有附件时显示文本 -->
              <div v-if="!task.file && !task.image" class="mt-2 text-light">
                No attachments available.
              </div>
            </div>
          </div>
          <div v-else>
            <p>Loading...</p>
          </div>
        </div>
        <div class="card-footer d-flex justify-content-between">
          <!-- 仅当用户为网红且任务状态为 available 时显示申请按钮 -->
          <button
            v-if="isInfluencer && task && task.status === 'available'"
            @click="applyForTask"
            class="btn btn-light text-primary btn-sm"
          >
            Apply for Task
          </button>
          <button @click="goBack" class="btn btn-secondary btn-sm">Back to Task List</button>
        </div>
      </div>
      <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
      <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  
  const API_BASE_URL = window.location.hostname === 'localhost'
? 'http://127.0.0.1:8000'
: 'https://influencer-platform-uecu.onrender.com';

  export default {
    name: 'TaskDetail',
    data() {
      return {
        task: null,
        isInfluencer: false,
        successMessage: '',
        errorMessage: '',
      };
    },
    mounted() {
      const taskId = this.$route.params.id;
      this.fetchTask(taskId);
      this.fetchUserRole();
    },
    methods: {
      fetchTask(taskId) {
        const token = localStorage.getItem('access_token');
        axios
          .get(`${API_BASE_URL}/api/tasks/${taskId}/`, {
            headers: {
              Authorization: 'Bearer ' + token,
            },
          })
          .then((response) => {
            this.task = response.data;
          })
          .catch((error) => {
            console.error('Error fetching task details:', error);
          });
      },
      fetchUserRole() {
        const token = localStorage.getItem('access_token');
        axios
          .get(`${API_BASE_URL}/api/me/`, {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            this.isInfluencer = response.data.role === 'influencer';
          })
          .catch((error) => {
            console.error('Error fetching user role:', error);
          });
      },
      applyForTask() {
        const token = localStorage.getItem('access_token');
        axios
          .post(
            `${API_BASE_URL}/api/tasks/${this.task.id}/apply/`,
            {},
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          )
          .then(() => {
            this.successMessage = 'Successfully applied for the task!';
            this.errorMessage = '';
          })
          .catch((error) => {
            console.error('Error applying for task:', error);
            if (error.response && error.response.data && error.response.data.detail) {
              const detail = error.response.data.detail;
              if (detail.includes('already applied')) {
                this.errorMessage = 'You have already applied for this task.';
              } else if (detail.includes('not available')) {
                this.errorMessage = 'This task is currently not available for application.';
              } else {
                this.errorMessage = detail;
              }
            } else {
              this.errorMessage = 'Failed to apply for the task. Please try again.';
            }
            this.successMessage = '';
          });
      },
      goBack() {
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
  .alert {
    max-width: 600px;
    margin: auto;
  }
  </style>
  