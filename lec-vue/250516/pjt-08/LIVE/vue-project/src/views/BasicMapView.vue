<template>
  <!-- <input v-model="keyword" @input="updateMap"/> <br> -->
  <iframe :src="mapUrl"></iframe>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const lat = ref(null)
const lng = ref(null)
const mapUrl = ref('')
// const keyword = ref('')

// 위치 정보 가져오기
const getCurrentLocation = () => {
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      lat.value = pos.coords.latitude
      lng.value = pos.coords.longitude
      updateMap() // 위치 받자마자 최초 1회 지도 표시
    },
  )
}

// iframe 지도 업데이트
const updateMap = () => {
  mapUrl.value =
    `https://maps.google.com/maps` +
    `?ll=${lat.value},${lng.value}` +
    `&z=14` +
    `&output=embed` 
    // + `&q=${keyword.value.trim()}`
}

// 초기 위치 설정
onMounted(() => {
  getCurrentLocation()
})

</script>
