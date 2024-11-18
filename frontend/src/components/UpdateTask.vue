<template>
    <div class="container my-5">
      <div class="card shadow-lg">
        <div class="card-header bg-primary text-white text-center">
          <h3>Update Task</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="updateTask" enctype="multipart/form-data">
            <div class="form-group mb-3">
              <label for="title" class="form-label">Title</label>
              <input type="text" v-model="task.title" class="form-control" required />
            </div>
            <div class="form-group mb-3">
              <label for="description" class="form-label">Description</label>
              <textarea v-model="task.description" class="form-control" required></textarea>
            </div>
            <div class="form-group mb-3">
              <label for="budget" class="form-label">Budget</label>
              <input type="number" v-model="task.budget" class="form-control" required />
            </div>
            <div class="form-group mb-3">
              <label for="deadline" class="form-label">Deadline</label>
              <input type="date" v-model="task.deadline" class="form-control" required />
            </div>
  
            <!-- 文件上传部分 -->
            <div class="form-group mb-3">
              <label for="file" class="form-label">File Attachment</label>
              <input type="file" @change="handleFileUpload" class="form-control" />
              <div v-if="task.file" class="mt-2">
                <p>Current File: <a :href="task.file" target="_blank" download>{{ task.file_name }}</a></p>
                <button type="button" @click="removeFile" class="btn btn-sm btn-danger">Remove File</button>
              </div>
            </div>
  
            <!-- 图片上传部分 -->
            <div class="form-group mb-3">
              <label for="image" class="form-label">Image Attachment</label>
              <input type="file" @change="handleImageUpload" class="form-control" />
              <div v-if="task.image" class="mt-2">
                <p>Current Image:</p>
                <img :src="task.image" alt="Task Image" class="img-fluid mb-2" />
                <button type="button" @click="removeImage" class="btn btn-sm btn-danger">Remove Image</button>
              </div>
            </div>
  
            <button type="submit" class="btn btn-success">Save Changes</button>
            <button @click="goBack" class="btn btn-secondary ms-3">Cancel</button>
          </form>
        </div>
      </div>
      <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  const API_BASE_URL = window.location.hostname === 'localhost'
? 'http://127.0.0.1:8000'
: 'https://influencer-platform-uecu.onrender.com';

  
  export default {
    name: 'UpdateTask',
    data() {
      return {
        task: {
          title: '',
          description: '',
          budget: null,
          deadline: '',
          file: null,
          image: null
        },
        newFile: null, // 新的文件
        newImage: null, // 新的图片
        errorMessage: ''
      };
    },
    created() {
      this.fetchTask();
    },
    methods: {
      fetchTask() {
        const token = localStorage.getItem('access_token');
        const taskId = this.$route.params.id;
        axios
          .get(`${API_BASE_URL}/api/tasks/${taskId}/`, {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then(response => {
            this.task = response.data;
          })
          .catch(() => {
            this.errorMessage = 'Failed to load task data.';
          });
      },
      handleFileUpload(event) {
        this.newFile = event.target.files[0];
      },
      handleImageUpload(event) {
        this.newImage = event.target.files[0];
      },
      removeFile() {
        this.task.file = null;
      },
      removeImage() {
        this.task.image = null;
      },
      updateTask() {
        const token = localStorage.getItem('access_token');
        const taskId = this.$route.params.id;
        
        // 创建表单数据对象以支持文件上传
        let formData = new FormData();
        formData.append('title', this.task.title);
        formData.append('description', this.task.description);
        formData.append('budget', this.task.budget);
        formData.append('deadline', this.task.deadline);
  
        // 检查是否上传新文件或删除旧文件
        if (this.newFile) {
          formData.append('file', this.newFile);
        } else if (!this.task.file) {
          formData.append('file', ''); // 表示删除文件
        }
  
        // 检查是否上传新图片或删除旧图片
        if (this.newImage) {
          formData.append('image', this.newImage);
        } else if (!this.task.image) {
          formData.append('image', ''); // 表示删除图片
        }
  
        axios
          .put(`${API_BASE_URL}/api/tasks/${taskId}/update/`, formData, {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            },
          })
          .then(() => {
            this.$router.push('/my-tasks');
          })
          .catch(() => {
            this.errorMessage = 'Failed to update task.';
          });
      },
      goBack() {
        this.$router.push('/my-tasks');
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
    font-weight: bold;
  }
  </style>
  