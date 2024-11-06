<template> 
    <div class="container my-5">
      <div class="card shadow-lg">
        <div class="card-header text-center bg-primary text-white">
          <h3 class="mb-0">My Posted Tasks</h3>
        </div>
        <div class="card-body">
          <div v-if="tasks.length === 0">
            <p>No tasks found.</p>
          </div>
          <table v-else class="table table-hover">
            <thead>
              <tr>
                <th>Task Name</th>
                <th>Status</th>
                <th>Applicants</th>
                <th>Deadline</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in tasks" :key="task.id">
                <td>{{ task.title }}</td>
                <td>{{ task.status }}</td>
                <td>{{ task.applicants_count || 0 }}</td>
                <td>{{ task.deadline }}</td>
                <td>
                  <button
                    v-if="task.status !== 'completed'"
                    @click="goToUpdateTask(task.id)"
                    class="btn btn-sm btn-warning"
                  >
                    Update
                  </button>
                  <button
                    v-if="task.status === 'available'"
                    @click="deleteTask(task.id)"
                    class="btn btn-sm btn-danger ms-2"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer text-center">
          <button @click="goToProfile" class="btn btn-secondary btn-sm">Back to Profile</button>
        </div>
      </div>
      <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'MyTasks',
    data() {
      return {
        tasks: [],
        errorMessage: '',
      };
    },
    mounted() {
      this.fetchTasks();
    },
    methods: {
      fetchTasks() {
        const token = localStorage.getItem('access_token');
        axios
          .get('http://127.0.0.1:8000/api/my-posted-tasks/', {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            this.tasks = response.data;
          })
          .catch((error) => {
            this.errorMessage = 'Failed to fetch tasks. Please try again.';
            console.error(error);
          });
      },
      goToProfile() {
        this.$router.push('/profile');
      },
      goToUpdateTask(taskId) {
        this.$router.push({ name: 'UpdateTask', params: { id: taskId } });
      },
      deleteTask(taskId) {
        const token = localStorage.getItem('access_token');
        axios
          .delete(`http://127.0.0.1:8000/api/tasks/${taskId}/delete/`, {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then(() => {
            this.tasks = this.tasks.filter(task => task.id !== taskId);
          })
          .catch((error) => {
            this.errorMessage = 'Failed to delete task. Please try again.';
            console.error(error);
          });
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
  