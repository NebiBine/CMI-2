<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';

const greeting = ref("")

function setGreeting() {
  const hour = new Date().getHours()

  if (hour < 12) {
    greeting.value = "Good Morning"
  } 
  else if (hour < 18) {
    greeting.value = "Good Afternoon"
  } 
  else {
    greeting.value = "Good Evening"
  }
}
onMounted(() => {
  setGreeting();
});

</script>
<template>
<h1>{{greeting}}, {{ username }}</h1>


</template>