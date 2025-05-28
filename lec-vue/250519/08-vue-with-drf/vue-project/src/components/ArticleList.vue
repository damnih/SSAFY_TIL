<template>
  <div>
    <h3>Article List</h3>
<!--     
    하위 컴포넌트에서 데이터 사용할 수 있도록 프랍 
-->
<!-- 이건 한마디로 articles 배열을 순회하며 각 아이템을 ArticleListItem으로 렌더링하는거   -->
    <ArticleListItem 
      v-for="article in store.articles" 
      :key="article.id"
      :article="article"
    />
  <!-- 프랍시켜주기 위해 여기서 article 바인딩까지 잘해주면 됨  -->
  </div>
</template>

<script setup>
  // 자식 컴포넌트 import
  import ArticleListItem from '@/components/ArticleListItem.vue'
  // Pinia 스토어 import 
  import { useArticleStore } from '@/stores/articles.js'
  // store.articles 에 접근 가능~~ 
  const store = useArticleStore() 

</script>
