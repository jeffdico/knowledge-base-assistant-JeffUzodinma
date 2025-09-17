<script setup>

import LoaderIndicator from "./Loader.vue"
  const props = defineProps({loading:Boolean})
  console.log(props.loading, " status value")

</script>
<template>
  <div class="minHeight border position-relative py-4 px-2">
    <p> Welcome to knowledge base. Where would you like to proceed today?</p>
    <loader-indicator v-if="props.loading">
       <template v-slot:title> Please wait for a response...</template>
    </loader-indicator>
  </div>
</template>
<style scoped>
  .minHeight {
      min-height: 500px;
      border-radius: 5px;
  }
</style>
