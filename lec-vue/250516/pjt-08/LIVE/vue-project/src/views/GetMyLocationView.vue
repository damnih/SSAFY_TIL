<template>
  <div>
    <button @click="loadLocation">내 위치 가져오기</button>
    <p v-if="lat && lng">Lat: {{ lat }}, Lng: {{ lng }}</p>
    <p v-if="error">{{ error }}</p>
  </div>
</template>
<script setup>
import { ref } from 'vue'

const lat = ref(null)
const lng = ref(null)
const error = ref('')

const loadLocation = () => {
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      lat.value = pos.coords.latitude
      lng.value = pos.coords.longitude
    },
    (err) => { 
      error.value = `위치 조회 실패: ${err.message}` 
    },
  )
}

</script>

