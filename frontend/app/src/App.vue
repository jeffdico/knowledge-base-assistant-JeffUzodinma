<script setup>
import {ref, onMounted} from "vue";
import BoxArea from "./components/Boxarea.vue"
import InputArea from './components/InputArea.vue'
import {GET, POST} from "./requests"

const category = ref("0");
const question = ref("");
const result = ref([]);
const result_notfound = ref(false);

const loading = ref(false);
const options = ref([{id: 1, value: 'sample data'}]);


onMounted(() =>{

  const on_success = (resp) => {
      options.value = resp.data;
  }
  const on_failed = (resp) => {
    console.log(resp.errormsg);
  }

  GET('/categorylist', on_success, on_failed)
})


function call_ai_func(){

    const on_success = (resp) => {
       loading.value = false;
       result.value = resp.data;
       if (!resp.data){
          result_notfound.value = true
       }
    }
    const on_failed = (resp) => {
      loading.value = false;

    }
    POST('/api/ask',
        {question: question.value, category: category.value},
        on_success, on_failed
      )
    result_notfound.value = false ;
    loading.value = true;

}
function field_change_func(field, value){

    if (field === "category"){
      category.value = value
    } else {
      question.value = value
    }
}

function browse_question_func(){

    const on_success = (resp) => {
      loading.value = false;
      result.value=resp.data;
      if (resp.data.length === 0){
        result_notfound.value = true
      }
    }
    const on_failed = (resp) =>  {
        console.log(resp.errormsg);
        loading.value = false;
    }

    GET("/api/search",
       on_success, on_failed, {},
      {query: question.value, category: category.value}
    );
    loading.value = true;
    result_notfound.value = false ;



}
</script>

<template>

    <div class="container">
      <div class="row">
          <div class="col-lg-12">

            <div class="d-flex justify-content-between align-items-center mb-0 mt-5">
              <h3 class="py-3 bold" style="width: 60%;"> Knowledge Base Assistant </h3>
              <p class="" style="width: 40%;">
                <select v-model="category" name="category" id="category" class="w-100 form-control">
                    <option value="0">Select Category</option>
                    <option :key='option.id' v-for="option in options" :value="option.id" :text="option.value"></option>
                </select>
              </p>
            </div>
          </div>
          <div class="col-lg-12 mb-3">
            <input-area @searchrequest="browse_question_func" @search_ai="call_ai_func" @update:value="field_change_func" :q="question" :category="category"></input-area>
          </div>
        <div class="col-lg-12">

            <box-area :loading="loading" :payload="result" :not_found="result_notfound"></box-area>

          </div>
      </div>

    </div>
</template>

<style scoped>
   .bold {
      font-weight: bold;
   }
</style>
