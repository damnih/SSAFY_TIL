<template>
  <h1> ChildItem </h1>
  <p>{{ item.id }}</p>
  <p>{{ item.name }}</p>
  <button @click="$emit('someEvent')">클릭 </button>
</template>

<script setup>
  const props = defineProps({
    item: Object
  })
  const emit = defineEmits(['someEvent'])
  const buttonClick = function () {
    // 여기서 복잡한 로직을 실행할 수도 있음 
    emit('someEvent', props.item, '구아바' )
  }


</script>

<style scoped>

</style>