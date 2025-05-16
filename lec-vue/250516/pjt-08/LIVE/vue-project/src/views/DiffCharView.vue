<template>
  <div>
    <h2>diffChars - 변환 구조</h2>
    <ul>
      <li v-for="(change, index) in changes" :key="index">
        {{ change }}
      </li>
    </ul>
    <hr>

    <h2>diffChars 활용</h2>
    <ul>
      <span 
        v-for="(change, index) in changes" 
        :key="index"
        :class="{ add: change.added, removed: change.removed }"
      >
        {{ change.value }}
      </span>
    </ul>

    <h3>diffChars 활용 2</h3>
    <p>변경된 단어 수: {{ diffCount }}</p>
  </div>
</template>

<script setup>
import { diffChars } from 'diff'

const oldStr = '변경 전'
const newStr = '변경 후 추가' 
const changes = diffChars(oldStr, newStr)
/* 
  [
    { value:'...', added?:true, removed?:true, count:n }, 
  …]

  [ 
    { "count": 3, "added": false, "removed": false, "value": "변경 " }, 
    { "count": 1, "added": false, "removed": true, "value": "전" }, 
    { "count": 4, "added": true, "removed": false, "value": "후 추가" } 
  ]
*/

// diffChars 활용 2
const diffCount = changes
  // 추가 되었거나 제거된 문자열만 filter
  .filter(function (char) {
    return char.added || char.removed
  })
  // 총 변경 단어 수를 count
  .reduce(function(sum, char) {
    return sum + char.count
  }, 0)

</script>

<style scoped>
 .add {
  color: green;
 }

 .removed {
  color: red;
  text-decoration: line-through;
 }
</style>