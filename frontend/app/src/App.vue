<script setup>
import {ref} from "vue";
import BoxArea from "./components/Boxarea.vue"
import InputArea from './components/InputArea.vue'

const category = ref("");
const question = ref("");
const loading = ref(false);

function call_ai_func(cat, q){


    console.log(cat);
    console.log(q);

    loading.value = true;
    setTimeout(()=>  loading.value = false, 10000)

}
function field_change_func(field, value){

    if (field === "category"){
      category.value = value
    } else {
      question.value = value
    }
}
</script>

<template>

    <div class="container">
      <div class="row">

          <div class="col-lg-12">  <h3 class="py-3 mb-0 mt-5 bold"> Knowledge Base Assistant </h3> </div>
          <div class="col-lg-8">

              <box-area :loading="loading"></box-area>

          </div>
          <div class="col-lg-4">
              <input-area @searchrequest="call_ai_func" @update:value="field_change_func" :q="question" :category="category"></input-area>

          </div>
      </div>

    </div>
</template>

<style scoped>
   .bold {
      font-weight: bold;
   }
</style>
