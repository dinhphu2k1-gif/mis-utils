<template>
  <div class="app-container">
    <Sidebar />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'

export default {
  components: { Sidebar }
}
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
}
.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>