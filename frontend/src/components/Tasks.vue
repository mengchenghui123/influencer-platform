<template>
  <div class="container">
    <h2>All Tasks</h2>
    
    <!-- 任务筛选和搜索行 -->
    <div class="d-flex mb-3 align-items-center">
      <!-- 任务状态筛选器 -->
      <div class="me-3">
        <label for="statusFilter" class="form-label">Filter by Status:</label>
        <select id="statusFilter" v-model="selectedStatus" @change="filterTasks" class="form-select">
          <option value="">All</option>
          <option value="available">Available</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      <!-- 任务搜索框 -->
      <div class="flex-grow-1">
        <label for="search" class="form-label">Search by Task Name or Posted By:</label>
        <input
          type="text"
          id="search"
          v-model="searchQuery"
          @input="filterTasks"
          class="form-control"
          placeholder="Enter task name or posted by"
        />
      </div>
    </div>

    <!-- 如果是商家，显示发布任务的按钮 -->
    <button v-if="isMerchant" @click="goToCreateTask" class="btn btn-primary mb-3">Post Task</button>

    <!-- 任务表格 -->
    <div v-if="filteredTasks.length === 0">No tasks available.</div>
    <table v-else class="table table-striped">
      <thead>
        <tr>
          <th scope="col">Task Name</th>
          <th scope="col">Posted By</th>
          <th scope="col">Status</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in filteredTasks" :key="task.id">
          <td>{{ task.title }}</td>
          <td>{{ task.posted_by }}</td>
          <td>{{ task.status }}</td>
          <td>
            <button @click="viewTask(task.id)" class="btn btn-info btn-sm">View Details</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TaskList',
  data() {
    return {
      tasks: [],
      filteredTasks: [],
      isMerchant: false,
      selectedStatus: '',
      searchQuery: '', // 搜索框的值
    };
  },
  mounted() {
    if (!localStorage.getItem('access_token')) {
      this.$router.push('/login');
    } else {
      this.checkAndReload(); // 调用检查刷新
      this.fetchUserRole();
      this.fetchTasks();
    }
  },
  methods: {
    checkAndReload() {
      if (localStorage.getItem('needsRefresh') === 'true') {
        localStorage.setItem('needsRefresh', 'false');
        location.reload();
      }
    },
    fetchUserRole() {
      const token = localStorage.getItem('access_token');
      axios
        .get('http://127.0.0.1:8000/api/me/', {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          this.isMerchant = response.data.role === 'merchant';
        })
        .catch((error) => {
          console.error('Error fetching user role:', error);
        });
    },
    fetchTasks() {
      const token = localStorage.getItem('access_token');
      axios
        .get('http://127.0.0.1:8000/api/tasks/', {
          headers: {
            Authorization: 'Bearer ' + token,
          },
        })
        .then((response) => {
          this.tasks = response.data;
          this.filterTasks();
        })
        .catch((error) => {
          console.error('Error fetching tasks:', error);
        });
    },
    filterTasks() {
      this.filteredTasks = this.tasks.filter((task) => {
        const matchesStatus = this.selectedStatus ? task.status === this.selectedStatus : true;
        const matchesSearch =
          task.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          task.posted_by.toLowerCase().includes(this.searchQuery.toLowerCase());
        return matchesStatus && matchesSearch;
      });
    },
    viewTask(taskId) {
      this.$router.push(`/tasks/${taskId}`);
    },
    goToCreateTask() {
      this.$router.push('/create-task');
    },
  },
  watch: {
    selectedStatus() {
      this.filterTasks();
    },
    searchQuery() {
      this.filterTasks();
    },
  },
  beforeRouteEnter(to, from, next) {
    if (to.name === 'Tasks' && from.name === 'Login') {
      localStorage.setItem('needsRefresh', 'true');
    }
    next();
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}
</style>
