<template>
  <div>
    <h1>CREATE PAGE</h1>
    <form @submit.prevent="createArticle" >
      <label for="title">title: </label>
      <input type="text" id="title" v-model="title">

      <label for="content">content: </label>
      <textarea id="content" v-model="content"> </textarea>
      <!-- <input type="text" id="content" v-model="content"> -->

      <input type="submit" value="[CREATE]">
    </form>
  </div>
</template>

<script setup>
  // 준비물
  // 1. axios
  import axios from 'axios'
  // 2. 게시글 상세 조회 요청 경로: 출처가 이미 스토어에 있음 
  import { useArticleStore } from '@/stores/articles.js'
  // 3. 응답 받은 게시글을 저장할 위치: 반응성 
  import { ref } from 'vue'
  // 4. 게시글 생성 완료 후 router.path
  import { useRouter } from 'vue-router'

  const title = ref(null)
  const content = ref(null)

  const store = useArticleStore()

  const createArticle = function () {
    axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/articles/`
      data: {
        title: title.value,
        content: content.value
      }
    })   
      .then(res => {
        console.log(res)
        console.log(res.data)
        // 정상적으로 인풋이 왓을 때, 페이지를 바꿔주고 싶음!!
        // 게시글 생성 완료 후, 그 게시글로 리다이렉트 되게 하는 거임 
        router.push({name: 'DetailView', params: { id: res.data.id }})
      }) 
      .catch(err => console.log(err))
  }


</script>

<style>

</style>
