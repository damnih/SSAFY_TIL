
<script setup>
  import { useCounterStore } from "../stores/counter.js"

  const store = useCounterStore()
  console.log(store)


</script>



<template>
  <div>
    <h1>Example</h1>
    <p> state: {{ store.count }}   </p>
    <p> getters: {{ store.doubleCount }}   </p>
    <button @click="store.increment">click</button>
  </div>



</template>



<style scoped>

</style>
