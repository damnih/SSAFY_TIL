<template>
  <div class="search-box">
    <h2>은행 찾기</h2>

    <label for="sido">광역시 / 도</label>
    <select id="sido" v-model="selectedSido">
      <option disabled value="">광역시 / 도를 선택하세요</option>
      <option 
        v-for="sido in mapInfo" 
        :key="sido.name" 
        :value="sido.name"
      >
        {{ sido.name }}
      </option>
    </select>

    <label for="sigungu">시 / 군 / 구</label>
    <select id="sigungu" v-model="selectedSigungu">
      <option disabled value="">시 / 군 / 구를 선택하세요</option>
      <option 
        v-for="sigungu in sigunguOptions" 
        :key="sigungu" 
        :value="sigungu"
      >
        {{ sigungu }}
      </option>
    </select>

    <label for="bank">은행</label>
    <select id="bank" v-model="selectedBank">
      <option disabled value="">은행을 선택하세요</option>
      <option 
        v-for="bank in bankInfo" 
        :key="bank" 
        :value="bank"
      >
        {{ bank }}
      </option>
    </select>

    <button @click="onSearch">찾기</button>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const mapInfo        = ref([])    // data.json 의 mapInfo
const bankInfo       = ref([])    // data.json 의 bankInfo
const selectedSido   = ref('')    // 선택된 광역시/도
const selectedSigungu= ref('')    // 선택된 시/군/구
const selectedBank   = ref('')    // 선택된 은행

// 1) data.json 을 fetch 해서 mapInfo/bankInfo 에 저장
onMounted(async () => {
  try {
    const res  = await fetch('/data.json')
    console.log('fetch status:', res.status)  
    if (!res.ok) throw new Error('데이터를 불러오는 데 실패했습니다.')
    const json = await res.json()
    console.log('json.mapInfo:', json.mapInfo)  
    mapInfo.value  = json.mapInfo     // [{ name: '서울특별시', countries: [...] }, ...]
    bankInfo.value = json.bankInfo    // ['국민은행', '신한은행', ...]
  }
  catch (e) {
    console.error(e)
  }
})

// 2) selectedSido 에 따라 sigunguOptions 동적 계산
const sigunguOptions = computed(() => {
  const entry = mapInfo.value.find(m => m.name === selectedSido.value)
  return entry ? entry.countries : []
})

// 3) 검색 버튼 핸들러 (예시)
function onSearch() {
  if (!selectedSido.value || !selectedSigungu.value || !selectedBank.value) {
    return alert('모든 항목을 선택하세요.')
  }
  const keyword = `${selectedSigungu.value} ${selectedBank.value}`
  console.log(' 검색 키워드:', keyword)
  
  // …카카오 맵 API 로 검색 처리…
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
/* 기존 CSS 그대로 옮기시면 됩니다 */
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
