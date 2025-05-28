<template>
  <header>
    <nav>
      <!-- Articles 링크 클릭 시 이름 ArticleView 라우트로 이동  -->
      <RouterLink :to="{ name:'ArticleView' }"> 
        Articles 
      </RouterLink>
    </nav>
  </header>
<!-- 여기서 라우터뷰를 쓰는 이유? 
현재 활성화된 라우트 컴포넌트를 렌더링하기 위함임  -->
  <RouterView />
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router'
</script>

<style scoped>
</style>
