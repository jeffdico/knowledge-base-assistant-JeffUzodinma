<script setup>

import LoaderIndicator from "./Loader.vue"
const props = defineProps({loading:Boolean, payload: Array(Object), not_found:Boolean})

</script>
<template>
  <div class="minHeight border position-relative py-4 px-4">

        <p v-if="props.payload.length===0 && !props.not_found" class="d-flex justify-content-center align-items-center">
            Welcome to knowledge base. What programming topic would you like to learn?
        </p>
        <div class="mb-3" v-for="(item, index) in props.payload" :key="index">
            <div v-if="item.search_type === 'local'">

                <p class="mb-1 border alert alert-warning rounded-lg p-3"> {{ item.result }} </p>
                <p class="text-muted"> <small> {{ item.aurthor }} | {{item.date}}  </small> </p>
            </div>
            <div v-if="item.search_type ==='ai'">
              <p class="mb-1">
                Based on your question : {{ item.question }}?
              </p>
              <p class="border alert alert-warning rounded-lg p-3">
                {{ item.result }}
              </p>
              <p class="text-muted"> <small>  {{ item.aurthor }} | {{ item.date }} </small> </p>

            </div>



        </div>

      <p class="alert alert-danger" v-if="props.not_found">
          No data found
      </p>


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
