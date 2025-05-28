// store/articles.js

import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useArticleStore = defineStore('article', () => {
  // 해야 할 일 
  // 1. axios 요청으로 api/v1/articles에 GET요청을 보낼 함수를 작성
  // 2. 그 게시글 조회 함수를 어딘가에서 요청을 보내야 한다 
  
  const articles = ref([
      { id: 1, title: 'title 1', content: 'content 1'},
      { id: 2, title: 'title 2', content: 'content 2'}, 
    ])

  // const API_URL = ''

  const getArticle = function () {
    axios({
      method: 'GET', 
      // 자주 요청을 보내게 될 API URL... 걍 변수로 관리해줄까?? 
      url: `${API_URL}/api/v1/articles/`
    })
      .then(res => {
        // console.log(res)
        // console.log(res.data) // array
        articles.value = res.data 


      })
  }



  return { 
    articles, API_URL,
    getArticle,
  }
}, { persist: true })
