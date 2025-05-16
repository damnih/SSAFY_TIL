<template>
  <h1>App.vue</h1>
    <!-- userName 변수에 든 값을 Parent 컴포넌트에게 Prop -->
    <!-- prop 받을 데이터가 담길 변수명은 html의 속성 형태로 작성  -->
      <!-- html의 기본 컨벤션은 케밥케이스  -->
      <!-- html의 속성에는 문자열만 담을 수 있다  -->
      <!-- 이제 숏컷할거임 바인딩할거임 -->

  <Parent 
    :user-name="userName"
    @change-user-name="onchangeUserName"
    />
</template>

<script setup>
  import Parent from './components/Parent.vue'
  // ref
  import { ref } from 'vue'
  const username = ref('Alice')
  const onChangeUserName = function () {
    userName.value = 'Charlie'
  }
</script>

<style scoped> 

</style>