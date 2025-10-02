<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';


const greeting = ref("")
const username = ref("")

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
  setGreeting()
  profilData()
});

async function profilData() {
  try {
    const response = await axios.get(
      'http://localhost:8080/data/getProfile', {
      withCredentials: true
    })
    //vzamem username 
    username.value = response.data.username

  }
  catch (error) {
    console.log('Napaka pri pridobivanju podatkov profila');
    console.log(error);
  }
};



</script>
<template>
  <div class="welcoming-block">
    <h1>{{ greeting }}, {{ username }}!</h1>
    <p>Your starting point for everything in CMI.</p>
  </div>
  <div class = "intro-block">
    <p>CMI connects you with essential urban services — from traffic updates and public transit to energy info and city guides. 
    Everything you need in one place.</p>
  </div>
  <div class = "quick-access">
    <h3>Quick Access</h3>
    <ul>
      <li>Traffic Updates</li>
      <li>Weather</li>
      <li>Public Transit</li>
      <li>Polls & Insights</li>
    </ul>
  </div>


</template>