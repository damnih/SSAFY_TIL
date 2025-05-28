<template>
  <div>
    <h1>Article Page</h1>

    <!-- 아티클 리스트 컴포넌트를 여기에 렌더링해서
    실제 글 목록을 보여줌  -->
    <ArticleList />

  </div>
</template>

<script setup>
  // 글 목록 컴포넌트 import
  import ArticleList from '@/components/ArticleList.vue'
  // 이건 Pinia 스토어 임포트해준거야 
  import { useArticleStore } from '@/stores/articles'
  // 이건 라이프사이클 훅Hook임 
  import { onMounted } from 'vue'
  
  const store = useArticleStore()
  
  // 이 컴포넌트가 mount 될 때 게시글 전체 조회
  // onMounted함수가 실행되었을 때, 나는 
  // 어떠한 일을 수행하도록 하고 싶어, -> 함수 실행
  // 그래 콜백함수가 필요할거같다 
  onMounted( () => {
    // 이거 원래 store.getArticles() 였는데 
    // 지피티가 이거 고치라고 알려줌 정의되어있지않대 
    store.getArticle()
  })
</script>

<style>

</style>
