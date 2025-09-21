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

  function trigger_search_ai(evt){
    evt.preventDefault();
    emit("search_ai")

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
    <div class="d-flex flex-row align-items-center ">
      <input v-model="q"
          class="form-control form-control-lg w-3.5" @keydown.enter.exact.prevent="trigger_search_emit"
          @input="trottle_update" name="q" id="q" placeholder="type your question"/>
      &nbsp; &nbsp;
      <button class="btn btn-success btn-lg w-10" title="browse the question" @click="trigger_search_emit"> Browse </button>
      &nbsp;&nbsp;
      <button class="btn btn-success btn-lg w-10" @click="trigger_search_ai" title="ask ai"> <i class="pi pi-microchip-ai"></i> </button>
    </div>
</div>
</template>

<!---->
<!-- -->
<style scoped>

</style>
