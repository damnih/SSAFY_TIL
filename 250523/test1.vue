
<template>

  <h1>근처의 은행 찾기 </h1>

  <div class="container">

    <div class="search-box">

      <h2>은행 찾기</h2>
      <!--   시/도 셀렉트 박스 부분  -->
      <label for="sido">광역시 / 도</label>
      <!-- v-model로 바인딩, 옵션은 mapInfo에서 동적으로 생성 -->
      <select id="sido" v-model="selectedSido">
        <option disabled value="">광역시 / 도를 선택하세요</option>
        <option
          v-for="item in mapInfo"
          :key="item.name"
          :value="item.name"
        >{{ item.name }}</option>
      </select>

      <!--   시/군/구 셀렉트 박스 부분 -->
      <label for="sigungu">시 / 군 / 구</label>
      <!-- v-model로 바인딩, selectedSido 변경 시 options 자동 업데이트 -->
      <select id="sigungu" v-model="selectedSigungu">
        <option disabled value="">시 / 군 / 구를 선택하세요</option>
        <option
          v-for="c in sigunguOptions"
          :key="c"
          :value="c"
        >{{ c }}</option>
      </select>

      <!--   은행 셀렉트 박스 부분    -->
      <label for="bank">은행</label>
      <!-- v-model로 바인딩, selectedSido 변경 시 은행 목록 설정 -->
      <select id="bank" v-model="selectedBank">
        <option disabled value="">은행을 선택하세요</option>
        <option
          v-for="b in bankInfo"
          :key="b"
          :value="b"
        >{{ b }}</option>
      </select>

      <!--   검색 버튼 부분          -->
      <button @click="onSearch">찾기</button>
    </div>

    <div id="map" ref="mapContainer"></div>
  </div>
</template>

<script setup>

import { ref, onMounted, computed } from 'vue'
import config from '../../apikey.js'

// mapInfo, bankInfo를 reactive하게 선언
const mapInfo = ref([])      // 원본 mapInfo 배열
const bankInfo = ref([])     // 원본 bankInfo 배열

// DOM에서 select 요소를 getElementById 했던 부분임.. 이걸 vue에서는 v-model 바인딩용 reactive 변수로 해결 
const selectedSido    = ref('')
const selectedSigungu = ref('')
const selectedBank    = ref('')

// const mapContainer = document.getElementById("map") 였던 걸 
// template ref로 연결
const mapContainer = ref(null)

// 마커 추적용 배열
let map, markers = [], infoWindow

// --- computed & lifecycle -------------------------------------------


// After: selectedSido 변화에 따라 시/군/구 목록 계산
const sigunguOptions = computed(() => {
  const found = mapInfo.value.find(m => m.name === selectedSido.value)
  return found ? found.countries : []
})


// 맵 초기화 & 데이터 로딩
onMounted(() => {
  // 1) Kakao SDK 스크립트 삽입
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${config.apikey}&autoload=false&libraries=services`
  script.onload = () => kakao.maps.load(initApp)
  document.head.appendChild(script)
})

async function initApp() {
  // Before: const res = await fetch('./data.json');
  //        const json = await res.json();
  // After: Vue state에 할당
  const res  = await fetch('./data.json')
  const json = await res.json()
  mapInfo.value  = json.mapInfo
  bankInfo.value = json.bankInfo

  // Before: new kakao.maps.Map(mapContainer, { … })
  // After: template ref를 사용
  map = new kakao.maps.Map(mapContainer.value, {
    center: new kakao.maps.LatLng(37.5665, 126.9780),
    level: 5
  })

  infoWindow = new kakao.maps.InfoWindow()
}

// --- 검색 핸들러 ---
function onSearch() {
  if (!selectedSido.value || !selectedSigungu.value || !selectedBank.value) {
    alert('모든 항목을 선택하세요.')
    return
  }

  const keyword = `${selectedSigungu.value} ${selectedBank.value}`
  const ps = new kakao.maps.services.Places()

  ps.keywordSearch(keyword, (result, status) => {
    if (status === kakao.maps.services.Status.OK) {
      // 기존 마커 제거
      markers.forEach(m => m.setMap(null))
      markers = []

      // 지도 범위 재설정
      const bounds = new kakao.maps.LatLngBounds()
      result.forEach(place => {
        const pos = new kakao.maps.LatLng(place.y, place.x)
        bounds.extend(pos)

        const marker = new kakao.maps.Marker({ map, position: pos })
        markers.push(marker)

        // 마커 클릭 시 인포윈도우
        kakao.maps.event.addListener(marker, 'click', () => {
          infoWindow.setContent(`<div style="padding:5px;">${place.place_name}</div>`)
          infoWindow.open(map, marker)
        })
      })
      map.setBounds(bounds)
    } else {
      alert('해당 지역에서 은행 정보를 찾을 수 없습니다.')
    }
  })
}
</script>

<style scoped>

body {
  font-family: sans-serif;
  padding: 20px;
}

.container {
  display: flex;
  gap: 20px;
}

.search-box {
  background-color: #e67e22;
  color: white;
  padding: 20px;
  width: 300px;
}

.search-box h2 {
  margin-top: 0;
}

.search-box label {
  margin-top: 10px;
  display: block;
}

.search-box select,
.search-box button {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}

.search-box button {
  background-color: white;
  color: #e67e22;
  border: none;
  font-weight: bold;
  cursor: pointer;
}

#map {
  width: 800px;
  height: 600px;
}

</style>
