<template>
  <div class="map-container">
    <input
      v-model="keyword"
      @input="tryUpdateMap"
      placeholder="키워드를 입력하고 Enter를 누르세요"
    />
    <iframe
      v-if="mapUrl"
      :src="mapUrl"
      width="100%"
      height="450"
      style="border:0; margin-top:1rem;"
      allowfullscreen
      loading="lazy"
    ></iframe>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { diffChars } from 'diff'

// 키워드와 이전 키워드 비교
const keyword = ref('')
const prevKeyword = ref('')

// 위도 경도 에러
const lat = ref(null)
const lng = ref(null)
const error = ref('')

const mapUrl = ref('')

// 위치 정보 가져오기
const getCurrentLocation = () => {
  navigator.geolocation.getCurrentPosition(
    pos => {
      lat.value = pos.coords.latitude
      lng.value = pos.coords.longitude
      error.value = ''
      updateMap() // 위치 받자마자 최초 1회 지도 표시
    },
    err => {error.value = err.message},
  )
}

// diff로 키워드 변화 판단 및 지도 갱신 시도
const tryUpdateMap = () => {
  const changes = diffChars(prevKeyword.value, keyword.value)
  const diffCount = changes
  // 추가 되었거나 제거된 문자열만 filter
  .filter(function (char) {
    return char.added || char.removed
  })
  // 총 변경 단어 수를 count
  .reduce(function(sum, char) {
    return sum + char.count
  }, 0)

  const threshold = 2 // 최소 두 글자 이상 바뀌어야 지도 업데이트
  if (diffCount >= threshold) {
    updateMap()
  } else {
    error.value = '키워드가 크게 바뀌지 않았습니다.'
  }
}

// iframe 지도 업데이트
const updateMap = () => {
  // 키워드가 비어있으면 현재 위치로 설정
  const query = keyword.value.trim() 
  ? keyword.value 
  :`${lat.value},${lng.value}`

  mapUrl.value =
    `https://maps.google.com/maps` +
    `?q=${query}` +
    `&ll=${lat.value},${lng.value}` +
    `&z=14` +
    `&output=embed`

  prevKeyword.value = keyword.value // 현재 키워드 저장
  error.value = ''
}

// 초기 위치 설정
onMounted(() => {
  getCurrentLocation()
})
</script>

<style scoped>
.map-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.error {
  color: #dc2626;
  margin-top: 1rem;
}
</style>
