<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { NAlert, NButton } from 'naive-ui'
import '../assets/styles/mainStyle.css';
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';
import { message } from "ant-design-vue";
import { createSwapy } from 'swapy'



const greeting = ref("");
const username = ref("");
const admin_state = ref(false);
const showAlert = ref(true);
const announcements = ref([]);
const swapy = ref(null);



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


async function profilData() {
  try {
    const response = await axios.get(
      'http://localhost:8000/auth/getProfile', {
      withCredentials: true
    })
    //vzamem username 
    username.value = response.data.username
    //message.success(response.data.message);
  }
  catch (error) {
    console.log('Napaka pri pridobivanju podatkov profila');
    //message.error(error.response.data.error);
    console.log(error);
  }
};
async function getAnnouncement(){
  try{
    const response = await axios.get(
      'http://localhost:8000/dashboard/getAnnouncement', 
      {withCredentials: true});
      announcements.value = response.data;
  }
  catch (error) {
    console.log('Error while fetching announcements');
    console.log(error);
  }
}

onMounted(() => {
  setGreeting(),
  profilData(),
  getAnnouncement()
  
  // Initialize Swapy
  const container = document.querySelector('.widgetsWrapper')
  if (container) {
    swapy.value = createSwapy(container, {
      animation: 'dynamic'
    })
  }
});


onUnmounted(() => {
  if (swapy.value) {
    swapy.value.destroy()
  }
});
</script>
<template>

<div v-for="announcement in announcements" :key="announcement.id">
    <n-alert :type="announcement.type" closable :title="announcement.title" >
      {{ announcement.content }}
    </n-alert>
  </div>


  <div class="welcoming-block">
    <h1>{{ greeting }}, {{ username }}!</h1>
    <p>CMI connects you with essential urban services — from traffic updates and public transit to energy info and city guides. 
      Everything you need in one place.</p>
  </div>
  <div class="widgetsWrapper">
    <div data-swapy-slot="poll-rewards">
      <div class="PollRewardsWidget" data-swapy-item="poll-rewards-widget">
        <h2>Polls & Rewards Overview</h2>
      </div>
    </div>
    
    <div data-swapy-slot="traffic">
      <div class="TrafficUpdatesWidget" data-swapy-item="traffic-widget">
        <h2>Traffic Overview</h2>
      </div>
    </div>
    
    <div data-swapy-slot="weather">
      <div class="WeatherWidget" data-swapy-item="weather-widget">
        <h2>Weather Overview</h2>
      </div>
    </div>
    
    <div data-swapy-slot="energy">
      <div class="EnergyInfoWidget" data-swapy-item="energy-widget">
        <h2>Energy Overview</h2>
      </div>
    </div>
  </div>



  <div class = "quick-access">

  </div>


</template>