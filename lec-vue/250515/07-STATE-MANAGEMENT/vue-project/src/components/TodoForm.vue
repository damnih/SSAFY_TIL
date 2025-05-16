<template>
  <!-- Q질문!! store.addTodo(todoText) 이렇게 써도 된다? O/X -->


  <form @submit.prevent="addTodo">
    <input type="text" v-model="todoText">
    <button>CREATE</button>
  </form>
</template>

<script setup>
  import { ref } from 'vue'
  import { useCounterStore } from '@/stores/counter.js'
  const store = useCounterStore()

  const todoText = ref('')
  const addTodo = function () {
    // 추가 로직 작성하려고...
    // 이 컴포넌트를 위한 함수로써 기능하도록 
    store.addTodo(todoText)
    todoText.value = ''

  }
</script>

<style scoped>

</style>