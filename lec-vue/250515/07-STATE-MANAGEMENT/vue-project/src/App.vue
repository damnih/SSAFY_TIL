<script setup>
  // 난이제 투두폼을 여기에 보여주게 하고 싶으니깐 아래 내용은 일단 싹 지울게 
  
  // import { useCounterStore } from "./stores/counter.js"

  // const store = useCounterStore()
  // console.log(store)

  import TodoForm from '@/components/TodoForm.vue'
  import TodoList from '@/components/TodoList.vue'

</script>



<template>
  <div>
    <h1>Todo Project</h1>
    <TodoForm />
    <TodoList />



<!-- 
    <p> state: {{ store.count }}   </p>
    <p> getters: {{ store.doubleCount }}   </p>
    <button @click="store.increment">click</button>
     -->
    <!-- 이렇게 익잼플 컴포넌트를 불러오면 걍 머 ,, 같은 내용이 두번 뜨겠지 ㅎ  -->
    <!-- <hr>
    <Example /> -->

  </div>



</template>



<style scoped>

</style>
