<template>
  <h1>Parent</h1>
  <p>{{ userName }}</p>
  <Child 
    :user-name="userName" 
    parent-name="Bella"
    @change-user-name="$emit('changeUserName')"
  />
</template>

<script setup>
  import Child from './Child.vue'
  // prop 정보를 정의하는 방법은 여러가지
  defineProps({
    // HTML 속성은 케밥케이스지만,
    // JS 변수명은 카멜케이스가 기본 컨벤션
    userName: String
    // userName: {
    //   type: String,
    //   required: true
    // }
  })
</script>

<style scoped>

</style>