<template>
  <div v-if="article">
    <h5>{{ article.id }}</h5>
    <p>{{ article.title }}</p>
    <p>{{ article.content }}</p>
    <p>{{ article.created_at }}</p>
    <p>{{ article.updated_at }}</p>
  </div>
</template>

<script setup>
  // 준비물
  // 1. axios
  import axios from 'axios' 
  // 2. 게시글 상세 조회 요청 경로: 출처가 이미 스토어에 있음
  import { useArticleStore } from '@/stores/articles.js'
  // 3. 조회 하고자 하는 게시글 id:route 
  import { useRoute } from 'vue-router'
  // 4. 응답 받은 게시글을 저장할 위치: 반응성 
  import { ref, onMounted } from 'vue'

  const article = ref(null)
  const store = useArticleStore()
  const route = useRoute()
  // 이 함수가 실행되면 params 에 있는 id를 기준으로, 
  // 게시글 상세 조회 요청을 보낸다. 

  const getArticle = function () {
    axios({
      method: 'GET',
      url: `${store.API_URL}/api/v1/articles/${route.params.id}/`
    })
    .then(res => {
      console.log(res)
      console.log(res.data)
    })
    .catch(err => console.log(err))
  }
  onMounted(() => {
    getArticle()
  })

</script>

<style>

</style>
