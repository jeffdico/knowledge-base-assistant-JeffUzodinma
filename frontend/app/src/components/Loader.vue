<script setup>
</script>
<template>
   <div class="abs w-100 h-100 z-99 d-flex align-items-center justify-content-center">
     <p class="text-center">
        <i class="pi pi-spin pi-spinner-dotted" style="font-size: 2rem"></i>
        <br/>
        <slot name="title"></slot> <br/>

     </p>
   </div>
</template>

<style scoped>
 .abs {
   position : absolute;
   top: 0; left: 0;
   background-color: #7777772b;
   color: #1e1d1d6e;
   text-shadow: 0px 1px 2px #fff;
   font-weight: bold;
 }

</style>
