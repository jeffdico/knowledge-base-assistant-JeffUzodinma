<script setup>

  import {ref} from "vue";

  const category = ref("");
  const q = ref("");

  const props = defineProps({category:String, question:String})

  const emit = defineEmits(["searchrequest","update:value"])
  function trigger_search_emit(evt){
      evt.preventDefault();
      emit("searchrequest", category.value, q.value); // for the the button is clicked
  }

  function trottle_update(evt){

      let name=evt.target.name, value=evt.target.value ;
      if (name == 'category'){
          category.value = value;
      } else {
          q.value = value
      }

      emit("update:value", name, value);
  }

</script>
<template>
<div class="mt-5">
    <div class="mb-4">
      <label for="category"> Study Category </label>
      <select v-model="category" @input="trottle_update" name="category" id="category" class="form-control form-control-lg mb-2">
        <option value="0"> Select Category </option>
      </select>
    </div>
    <div class="mb-4">
      <label for="q"> Enter your Question </label>
      <textarea v-model="q" rows="5" cols="5"
          class="form-control form-control-lg mb-4"
          @input="trottle_update" name="q" id="q" placeholder="type your question here"/>
    </div>
    <div class="mt-4">
      <button class="btn btn-success btn-lg w-100" @click="trigger_search_emit"> Submit <i class="pi pi-send" style="color: white"></i></button>
    </div>
</div>
</template>

<style scoped>

</style>
