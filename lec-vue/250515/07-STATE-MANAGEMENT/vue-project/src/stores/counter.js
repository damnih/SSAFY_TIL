import { ref, computed } from 'vue'
import { defineStore } from 'pinia'


export const useCounterStore = defineStore('counter', () => {
  // 얘는 return 해야 할까? 
  let id = 0
  
  // 사용자가 값을 CUD 할 때 반응할 수 있도록 반응형으로 작성
  const todos = ref([
    // todo 객체 틀을 만든다 
    // input:checkbox에 쓰일 id도 필요하고, v-for로 순회할 때 쓸 key도 필요하다
    // 더미 데이터니깐,,, 1,2,3,4 할 수도 있는데,, 나중에 값이 추가됐을때도 처리! 
    {id: id++, text: 'vue 공부', isDone: false},
    {id: id++, text: 'django 공부', isDone: false},
    {id: id++, text: '걍 내 공부', isDone: false},
    {id: id++, text: 'JS 공부', isDone: false},
    // 이 id는 뷰에서 쓰는 게 아님 
    // 걍 이 내부에서만 쓰는 거야 
    // 상태변수만 리턴하기로 했었잖아! 
    // 이 id의 증감까지 vue가 추적할 필요는 없음~! 
    // 걍 그 단순히 로직을 위해 선언하는 변수도 필요한거임 
    // 사용자랑 상호작용하는 부분이 아니잖아 여기는! 
    // 그니깐 반환하지 않는 거임 
  ])

  return { todos }
}, {persist: true })

  const addTodo = function (todoText) {
    todos.value.push({
      id: id++,
      isDone: false,
      text: todoText
    })
  }

  const deleteTodo = function(selectedId) {
    // 넘겨받은 id값을 기준으로, 
    // 내가 가진 toods를 전체 순회하면서, 각각의 todo 객체가 가진 id와 비교한다.
    // 그리고 비교한 결과가 true인 값을 반환할대의 todo들만 모아서 새로운 배열ㅇ르 만든다. 
    todos.value = todos.value.filter(todo => todo.id != selectedId)
  }

  const updateTodo = function (selectedId) {
    todoe.value = todos.value.map((todo) => {
      if (todo.id === selectedId) {
        todo.isDone = !todo.isDone      
      }
      return todo 
    })
  }

  return {
    // 값 선언 했으면, 바로바로 까먹지 않도록 return 해주자
    todos, 
    addTodo, deleteTodo, updateTodo
  }




// export const useCounterStore = defineStore('counter', () => {
//   const count = ref(0)
//   const doubleCount = computed(() => count.value * 2)
//   function increment() {
//     count.value++
//   }

//   return { count, doubleCount, increment }
// })
