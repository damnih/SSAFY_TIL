

<template>
  <header>
    <nav>
      <RouterLink to="/">GetMyLocation</RouterLink> | 
      <RouterLink :to="{name: 'basicMap'}">basicMap</RouterLink> | 
      <RouterLink :to="{name: 'diffChar'}">diffChar</RouterLink> | 
      <RouterLink :to="{name: 'location'}">LocationMap</RouterLink> | 
    </nav>
  </header>
  <div class="container">
    <RouterView />
  </div>
</template>

<script setup>
  import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
  .container {
    width: 800px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ccc;
  }
</style>