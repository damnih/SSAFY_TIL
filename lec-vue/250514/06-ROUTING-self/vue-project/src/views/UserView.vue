<template>
  <div>
    <h1>User PAGE</h1>
    <button @click="goHome">Home!</button>


    <h2>현재 경로에 관련된 어떤 정보들은 {{ $route.params }}</h2>
    <h2>현재 경로에 관련된 어떤 정보들은 {{ $route.params.id }}</h2>
    <!-- post 혹은 profile로 이동할 수 있어야 한다
    = 링크가 필요하다
     -->
      <RouterLink :to="{name: 'user-profile'}" > Profile </RouterLink>
      <RouterLink :to="{name: 'user-post'}" > Posts </RouterLink>
    <!-- 만약 중첩된 자식들의 정보를 보여주고 싶어  -->
    <RouterView />
  
  </div>
</template>

<script setup>
  // import { RouterView } from ''
  // route 기능은 우리가 프로젝트에 추가한 vue-router가 가지고있음.
  import { useRoute, useRouter, RouterView, RouterLink } from 'vue-router'
    const route = useRoute()
    const router = useRouter()
    console.log(route)
    console.log(router)

    // 이제 저 위에서 정해뒀던 goHome이란 이름의 함수를 만들어주자  
    const goHome = function () {
      // 어디로? 이동?
      router.push({ name: 'home' })

      
    }



    // definePrams 
    // define어쩌구 그걸 이용해서 할수잇잖아 그거 기억 ㄱㄱ 


</script>

<style scoped>

</style>