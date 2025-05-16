<template>
  <div>
    <!-- 속성에 넣는 것과 template syntax 작성 방법이 다른 것 잊지 말기~!~!~!  -->
     <!-- 양방향 바인딩을 해줘야해서 브이모델 추가함 -->
    <input type="checkbox" :id="todo.id" v-model="todo.isDone">
<!--     
    label의 for와 같은 값을 가진 id를 찾아서 
    라벨에 작성된 텍스트 컨텐트를 클릭하면 
    찾아둔 동일 아이디를 가진 요소에 focus
     -->
    <label :for="todo.id">{{ todo.text }}</label>
    <button @click="onDeleteTodo">삭제</button>
  </div>

</template>

<script setup>
  import { useCounterStore } from '@/stores/counter.js'

  const props = defineProps({
    todo: Object
  })

  const store = useCounterStore()
  const onDeleteTodo = function () {
    // 상위 컴포넌트에서 프랍받은 todo를 쓰고 싶어요
    // 그렇다면 그냥 디파인프랍으로 정의하고 투두닷 쓰면 됨
    // 근데 만약 스크립트 영역에서 쓰고싶어 
    // 그렇다면
    // 그 프랍스가 받은 투두의 아이디를 써야 한다는 것 
    store.deleteTodo(Props.todo.id)
  }


</script>

<style scoped>

</style>