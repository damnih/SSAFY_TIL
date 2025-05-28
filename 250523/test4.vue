<template>
  <div class="container">
    <!-- 검색 박스 -->
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

    <!-- 지도가 그려질 영역 -->
    <div id="map" class="map-box"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
// @ 는 src/ 를 가리키는 alias. 필요하면 상대경로로 바꿔주세요.
import { config } from '@/apikey.js'

const API_KEY = config.API_KEY

// 드롭다운용 데이터
const mapInfo        = ref([])    // public/data.json → mapInfo
const bankInfo       = ref([])    // public/data.json → bankInfo
const selectedSido   = ref('')    // 광역시/도
const selectedSigungu= ref('')    // 시/군/구
const selectedBank   = ref('')    // 은행 종류

// 시/군/구 목록 자동 계산
const sigunguOptions = computed(() => {
  const found = mapInfo.value.find(m => m.name === selectedSido.value)
  return found ? found.countries : []
})

// 카카오맵 전역 변수들
let map, infoWindow
let markers = []

// 1) 런타임에 Kakao SDK를 동적 로드
function loadKakaoSdk(key) {
  return new Promise((resolve, reject) => {
    if (window.kakao && window.kakao.maps) {
      // 이미 로드되어 있으면 바로
      return resolve(window.kakao)
    }
    const script = document.createElement('script')
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${key}&libraries=services`
    script.onload = () => {
      window.kakao.maps.load(() => {
        resolve(window.kakao)
      })
    }
    script.onerror = () => reject(new Error('Kakao SDK 로드 실패'))
    document.head.appendChild(script)
  })
}

onMounted(async () => {
  console.log('▶︎ API_KEY is:', API_KEY)
  // 1) SDK 로드
  try {
    const kakao = await loadKakaoSdk(API_KEY)
    // 이제 window.kakao가 100% 보장됨
    const container = document.getElementById('map')
    map = new kakao.maps.Map(container, {
      center: new kakao.maps.LatLng(37.5665, 126.9780),
      level: 7
    })
    infoWindow = new kakao.maps.InfoWindow({ zIndex: 1 })
  } catch (e) {
    alert('지도 로드 실패')
  }

  // 2) data.json 가져와서 mapInfo, bankInfo 채우기
  try {
    const res  = await fetch('/data.json')
    if (!res.ok) throw new Error(res.statusText)
    const json = await res.json()
    mapInfo.value  = json.mapInfo
    bankInfo.value = json.bankInfo
  } catch (e) {
    console.error('data.json 불러오기 실패', e)
  }

  // 3) 지도 초기화
  const container = document.getElementById('map')
  map = new kakao.maps.Map(container, {
    center: new kakao.maps.LatLng(37.5665, 126.9780),
    level: 7
  })
  infoWindow = new kakao.maps.InfoWindow({ zIndex: 1 })
})

// 4) 검색 버튼 핸들러
function onSearch() {
  if (!selectedSido.value || !selectedSigungu.value || !selectedBank.value) {
    return alert('모든 항목을 선택하세요.')
  }

  // 이전 마커 제거
  markers.forEach(m => m.setMap(null))
  markers = []

  const keyword = `${selectedSigungu.value} ${selectedBank.value}`
  const ps = new kakao.maps.services.Places()

  ps.keywordSearch(keyword, (results, status) => {
    if (status === kakao.maps.services.Status.OK) {
      const bounds = new kakao.maps.LatLngBounds()
      results.forEach(place => {
        const pos = new kakao.maps.LatLng(place.y, place.x)
        bounds.extend(pos)

        const marker = new kakao.maps.Marker({ map, position: pos })
        markers.push(marker)

        kakao.maps.event.addListener(marker, 'click', () => {
          infoWindow.setContent(
            `<div style="padding:5px;">${place.place_name}</div>`
          )
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
.container {
  display: flex;
  gap: 20px;
}

/* 검색 박스 스타일 */
.search-box {
  width: 300px;
  background-color: #e67e22;
  color: white;
  padding: 20px;
  border-radius: 4px;
}

.search-box h2 {
  margin-top: 0;
}

.search-box label {
  display: block;
  margin-top: 10px;
}

.search-box select,
.search-box button {
  width: 100%;
  margin-top: 5px;
  padding: 8px;
  font-size: 14px;
}

.search-box button {
  background: white;
  color: #e67e22;
  border: none;
  font-weight: bold;
  cursor: pointer;
  border-radius: 2px;
}

/* 지도 박스 */
.map-box {
  flex: 1;
  height: 600px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
