<template>
  <h1>Child</h1>
  <p> {{ userName }} </p>
  <p> {{ parentName }} </p>
  <!-- ChildItem components는 Child.bue 가 가진 items 배열의 요소 수 만큼 만들 거다  -->
  <button @click="@emit('changeUserName')"> click!! </button>
  
  <ChildItem 
    v-for="item in items"
    :key="item.id"
    :item="item"
    @some-event="onSomeEvent"
  />
</template>

<script setup>
  import { ref } from 'vue'
  import ChildItem form './ChildItem.vue'
  defineProps({
    userName: String,
    parentName: String
  })
  const items = ref([
    {id: 1, name: '사과'}
    {id: 2, name: '바나나'}
    {id: 3, name: '딸기'}
  ])

  const onSomeEvent = function (arg, name) {
    console.log('데이터를 넘겨받음 ')
    for (let i=0; i<items.value.length+1; i+=1) {
      console.log(items.value[i])
      if (arg.id === items.value[i].id) {
        // items.value[i].name = '파인애플'
        items.value[i].name = name
      }
    }
  }
    // console.log('어떤 이벤트가 발생함 ')
    // console.log(item)
    // 넘겨받은 객체의 아이디값.. 은 어때?  
    // 객체 자체를 넘길 게 아니라 아이디만 넘겨도 될지도? 
    


</script>

<style scoped>

</style>