<template>
  <div class="sidebar">
    <h2>Menu</h2>
    <ul>
      <li>
        <router-link to="/leave-request">Xin nghỉ phép</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #f4f4f4;
  padding: 20px;
  border-right: 1px solid #ddd;
}
.sidebar h2 {
  margin-bottom: 20px;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  margin: 10px 0;
}
.sidebar a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}
.sidebar a:hover {
  color: #007bff;
}
</style>