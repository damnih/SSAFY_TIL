<!-- MyComponent.vue -> 이름은 PascalCase로 작성 -->
<template>
  <div>
    <h1>MyComponent</h1>
    <p>{{ massege }}</p>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  const massege = ref('값')
</script>

<style scoped>
  h1 {
    color:red
  }
</style>