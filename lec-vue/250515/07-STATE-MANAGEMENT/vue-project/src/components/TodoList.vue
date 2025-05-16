<template>
  <div>
    
<!--     
    v-for는 반복문을 실행한 것일 뿐이고, 
    TodoListItem 컴포넌트에게 todo 정보를 prop시켜주자! 
 -->

    <TodoListItem 
      v-for="todo in store.todos"
      :key="todo.id"
    
    
    />


    <!-- 나중에는 for문으로 반복할거임 -->
     <!-- 일단 화면 구성 확인을 위해서 무지성으로 3개 복붙해둘게  -->
<!-- 
     <TodoListItem />
    <TodoListItem />
    <TodoListItem />
 -->

  </div>
</template>

<script setup>
  import TodoListItem from '@/components/TodoListItem.vue'
  import { useCounterStore } from "@/stores/counter.js";

  const store = useCounterStore()

</script>

<style lang="scss" scoped>

</style>